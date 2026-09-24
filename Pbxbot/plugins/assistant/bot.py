import heroku3
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, Message, ReplyKeyboardRemove
from Pbxbot import HEROKU_APP
from Pbxbot.core import LOGS
from Pbxbot.functions.tools import restart
from ..btnsG import gen_bot_help_buttons, start_button
from . import HELP_MSG, START_MSG, BotHelp, Config, Pbxbot

@Pbxbot.bot.on_message(filters.command("restart"))
async def restart_cmd(_, message: Message):
    await message.reply_text(
        "**ʀᴇsᴛᴀʀᴛ** ᴅᴍ ɴᴏᴡ ᴍʏ ᴅᴇᴠ . [♡³_🫧𝆺꯭𝅥˶֟፝͟͝β𝝰꯭‌𝞉 ꯭𝝡꯭𝞄꯭𝞌𝞉꯭𝝺꯭𝆺꯭𝅥🍷┼❤️༆](https://t.me/PB_SUKH) 🙈❤️."
    )


@Pbxbot.bot.on_message(filters.command("start"))
async def start_pm(_, message: Message):
    btns = start_button()

    await message.reply_photo(
        photo="https://files.tgvibes.online/SgeylAxC.jpg",
        caption=START_MSG.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup(btns),
    )
    log_text = f"""
**ɴᴇᴡ ᴜsᴇʀ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ 🚀**

**ғɪʀsᴛ ɴᴀᴍᴇ:** {user.first_name}
**ᴜsᴇʀ ɪᴅ:** `{user.id}`
**ᴜsᴇʀɴᴀᴍᴇ:** @{user.username if user.username else "ɴᴏᴛ sᴇᴛ"}
"""
    try:
        await Pbxbot.bot.send_message(Config.LOGGER_ID, log_text)
    except Exception as e:
        LOGS.error(f"Failed to send start log: {e}")


@Pbxbot.bot.on_message(filters.command("help"))
async def help_pm(_, message: Message):
    btns = await gen_bot_help_buttons()
    await message.reply_text(
        HELP_MSG,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(btns),
    )


@Pbxbot.bot.on_message(filters.command("rs") & Config.AUTH_USERS)
async def restart_clients(_, message: Message):
    await message.reply_text("Restarted Bot Successfully ✅")
    try:
        if HEROKU_APP:
            try:
                heroku = heroku3.from_key(Config.HEROKU_APIKEY)
                app = heroku.apps()[Config.HEROKU_APPNAME]
                app.restart()
            except:
                await restart()
        else:
            await restart()
    except Exception as e:
        LOGS.error(e)
