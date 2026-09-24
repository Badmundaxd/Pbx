# Pbxbot/plugins/bot/session_cleandb.py
# ─── Database Cleaning Commands ───

from pyrogram import Client, filters
from pyrogram.errors import AuthKeyUnregistered, SessionRevoked, UserDeactivatedBan, UserDeactivated, ApiIdInvalid
from pyrogram.types import Message

from . import Config, db, Pbxbot


@Pbxbot.bot.on_message(filters.command("cleandb") & Config.AUTH_USERS & filters.private)
async def clean_expired_sessions(_, message: Message):
    msg = await message.reply_text("**🔍 Scanning all sessions...**\n\nThis may take a while.")

    total_checked = 0
    total_removed = 0
    results = []

    async def check_session(session_string, user_id, label, rm_func):
        nonlocal total_checked, total_removed
        total_checked += 1
        try:
            temp = Client(name=f"Check_{label}_{user_id}", session_string=session_string, api_id=Config.API_ID, api_hash=Config.API_HASH, in_memory=True)
            await temp.connect()
            try:
                await temp.get_me()
            except Exception:
                await temp.disconnect()
                await rm_func(user_id)
                total_removed += 1
                results.append(f"❌ {label} `{user_id}` — expired")
                return
            await temp.disconnect()
        except (AuthKeyUnregistered, SessionRevoked, UserDeactivatedBan, UserDeactivated, ApiIdInvalid):
            await rm_func(user_id)
            total_removed += 1
            results.append(f"❌ {label} `{user_id}` — expired")
        except Exception:
            pass

    for s in await db.get_all_sessions():
        uid = s.get("user_id"); ss = s.get("session_string") or s.get("session")
        if uid and ss: await check_session(ss, uid, "User", db.rm_session)

    text = (
        f"**✅ Session Scan Complete!**\n\n"
        f"**Total Checked:** `{total_checked}`\n"
        f"**Total Removed:** `{total_removed}`\n\n"
    )
    if results:
        text += "**Removed:**\n" + "\n".join(results[:20])
        if len(results) > 20:
            text += f"\n... and {len(results)-20} more"

    await msg.edit(text)


@Pbxbot.bot.on_message(filters.command("cleanalldb") & Config.AUTH_USERS & filters.private)
async def clean_entire_database(_, message: Message):
    await db.clean_all()
    await message.reply_text(
        "⚠️ 𝗪𝗔𝗥𝗡𝗜𝗡𝗚!\n\n"
        "𝖠𝗅𝗅 𝖽𝖺𝗍𝖺𝖻𝖺𝗌𝖾 𝖼𝗈𝗅𝗅𝖾𝖼𝗍𝗂𝗈𝗇𝗌 (𝗌𝖾𝗌𝗌𝗂𝗈𝗇𝗌, 𝖻𝖺𝗇𝗌, 𝗆𝗎𝗍𝖾𝗌, 𝖿𝗂𝗅𝗍𝖾𝗋𝗌, 𝗌𝗇𝗂𝗉𝗌, 𝗉𝗆𝗉𝖾𝗋𝗆𝗂𝗍𝗌, 𝖾𝗍𝖼.) 𝗁𝖺𝗏𝖾 𝖻𝖾𝖾𝗇 𝗐𝗂𝗉𝖾𝖽!\n"
        "__𝗍𝗁𝗂𝗌 𝖺𝖼𝗍𝗂𝗈𝗇 𝗂𝗌 𝗂𝗋𝗋𝖾𝗏𝖾𝗋𝗌𝗂𝖻𝗅𝖾 — 𝖺𝗅𝗅 𝖽𝖺𝗍𝖺 𝗂𝗌 𝗀𝗈𝗇𝖾 𝗉𝖾𝗋𝗆𝖺𝗇𝖾𝗇𝗍𝗅𝗒.__"
    )