# Pbxbot/plugins/bot/btnsK.py
from pyrogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


def gen_keyboard(collection: list, row: int = 2) -> list[list[KeyboardButton]]:
    keyboard = []
    for i in range(0, len(collection), row):
        kyb = []
        for x in collection[i : i + row]:
            kyb.append(KeyboardButton(x))
        keyboard.append(kyb)
    return keyboard


# ══════════════════════════════════════════════════
#  MAIN SESSION MENU
# ══════════════════════════════════════════════════

def session_main_keyboard() -> ReplyKeyboardMarkup:
    """Main session menu — choose session type"""
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("👤 ʙᴀsɪᴄ ᴜsᴇʀʙᴏᴛ"),
            ],
            [
                KeyboardButton("ʜᴏᴍᴇ ⚜️"),
            ],
        ],
        resize_keyboard=True,
    )


# ══════════════════════════════════════════════════
#  BASIC USERBOT SESSION
# ══════════════════════════════════════════════════

def session_keyboard() -> ReplyKeyboardMarkup:
    """Basic userbot session management"""
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("ɴᴇᴡ 🔮"),
                KeyboardButton("ᴅᴇʟᴇᴛᴇ 🚫"),
            ],
            [
                KeyboardButton("ʟɪsᴛ 📄"),
                KeyboardButton("ʜᴏᴍᴇ ⚜️"),
            ],
        ],
        resize_keyboard=True,
    )


# ══════════════════════════════════════════════════
#  MAIN BOT START KEYBOARD
# ══════════════════════════════════════════════════

def start_keyboard() -> ReplyKeyboardMarkup:
    """Main bot menu"""
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("👤 ᴍʏ ᴘʀᴏꜰɪʟᴇ"),
                KeyboardButton("📘 ʜᴏᴡ ᴛᴏ ᴜsᴇ"),
            ],
            [
                KeyboardButton("💰 ʙᴜʏ ᴄʀᴇᴅɪᴛs"),
                KeyboardButton("🎁 ʀᴇꜰᴇʀ"),
            ],
            [
                KeyboardButton("📳 sᴇssɪᴏɴ"),
            ],
            [
                KeyboardButton("❌ ᴄʟᴏsᴇ"),
            ],
        ],
        resize_keyboard=True,
    )

# ══════════════════════════════════════════════════
#  START REPLY KEYBOARD
# ══════════════════════════════════════════════════

def start_reply_keyboard() -> ReplyKeyboardMarkup:
    """Start command pe aane wala ReplyKeyboard — Help button included"""
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("📝 ʜᴇʟᴘ"),
                KeyboardButton("📳 sᴇssɪᴏɴ"),
            ],
            [
                KeyboardButton("ʜᴏᴍᴇ ⚜️"),
                KeyboardButton("❌ ᴄʟᴏsᴇ"),
            ],
        ],
        resize_keyboard=True,
    )
