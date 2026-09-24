import asyncio
import heroku3

from pyrogram import Client, filters, enums
from pyrogram.errors import (
    SessionPasswordNeeded,
    AuthKeyUnregistered,
    SessionRevoked,
    UserDeactivatedBan,
    UserDeactivated,
    ApiIdInvalid
)

from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    ReplyKeyboardRemove,
    KeyboardButton,
    ReplyKeyboardMarkup
)

from ..btnsG import gen_inline_keyboard, start_button
from ..btnsK import (
    session_keyboard,
    session_main_keyboard,
)

from . import START_MSG, BotHelp, Config, Symbols, db, Pbxbot
from Pbxbot.functions.tools import restart
from Pbxbot import HEROKU_APP


# ─────────────────────────────────────────────
# AUTO RESTART
# ─────────────────────────────────────────────

async def auto_restart():
    try:
        if HEROKU_APP:
            try:
                heroku = heroku3.from_key(Config.HEROKU_APIKEY)
                app = heroku.apps()[Config.HEROKU_APPNAME]
                app.restart()
            except Exception:
                await restart()
        else:
            await restart()

    except Exception as e:
        print(f"Auto restart error: {e}")


# ─────────────────────────────────────────────
# SESSION VALIDATOR
# ─────────────────────────────────────────────

def validate_session(session):
    """Validate session string format."""
    
    if session.startswith("==Pbx") and session.endswith("BadMunda=="):
        return session[5:-10]

    return None


# ─────────────────────────────────────────────
# SESSION MENU
# ─────────────────────────────────────────────

@Pbxbot.bot.on_message(filters.command("session"))
async def session_menu(_, message: Message):

    await message.reply_text(
        """
**┌────── ˹ sᴇssɪᴏɴ ᴍᴀɴᴀɢᴇʀ ˼ ⏤͟͞★**
**┆◍ ᴄʜᴏᴏsᴇ sᴇssɪᴏɴ ᴛʏᴘᴇ**
**└────────────────•**

**❖ ʙᴀsɪᴄ • sᴘᴀᴍ • ʙᴏᴛ**
**❖ ᴛɪᴍᴇʀ • ᴍᴇᴅɪᴀ sᴀᴠᴇ**
""",
        reply_markup=session_main_keyboard(),
    )


# ─────────────────────────────────────────────
# BASIC USERBOT
# ─────────────────────────────────────────────

@Pbxbot.bot.on_message(
    filters.regex(r"^👤 ʙᴀsɪᴄ ᴜsᴇʀʙᴏᴛ$") & filters.private
)
async def basic_userbot_menu(_, message: Message):

    await message.reply_text(
        """
**┌────── ˹ ʙᴀsɪᴄ ᴜsᴇʀʙᴏᴛ ˼ ⏤͟͞★**
**┆◍ ᴀʟʟ ʙᴀsɪᴄ ꜰᴇᴀᴛᴜʀᴇs**
**└────────────────•**

**◍ ʀᴀɪᴅ • ᴄʟᴏɴᴇ**
**◍ ᴛᴀɢɢᴇʀ • sᴘᴀᴍ**
**◍ ᴍᴇᴅɪᴀ sᴀᴠᴇ**
""",
        reply_markup=session_keyboard(),
    )


# ─────────────────────────────────────────────
# BOT CLONE
# ─────────────────────────────────────────────


# ─────────────────────────────────────────────
# HOME BUTTON
# ─────────────────────────────────────────────

@Pbxbot.bot.on_message(filters.regex(r"ʜᴏᴍᴇ ⚜️"))
async def go_home(_, message: Message):

    btns = start_button()

    # Remove reply keyboard silently
    try:
        temp_msg = await message.reply_text(
            "❤️",
            reply_markup=ReplyKeyboardRemove()
        )

        await temp_msg.delete()

    except Exception:
        pass

    # Send start message
    sent = await message.reply_photo(
        photo="https://files.tgvibes.online/SgeylAxC.jpg",
        caption=START_MSG.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup(btns),
        quote=False
    )

    # Auto delete after 5 sec
    await asyncio.sleep(5)

    try:
        await sent.delete()

    except Exception:
        pass


# ─────────────────────────────────────────────
# RESTART BUTTONS
# ─────────────────────────────────────────────

def restart_buttons() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📝 ʜᴇʟᴘ & ꜰᴇᴇᴅʙᴀᴄᴋ 💬",
                url="https://pbx4-0.vercel.app",
                style=enums.ButtonStyle.SUCCESS  # Green banao
            )
        ]
    ])
