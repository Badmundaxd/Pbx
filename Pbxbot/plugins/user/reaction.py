import asyncio

import aiohttp
from pyrogram import Client
from pyrogram.types import Message

from Pbxbot.bad.shizu import GetChatID, ReplyCheck
from . import HelpMenu, on_message


# ─────────────────────────────────────────────
#  HELPER — fetch GIF from waifu.pics & send
# ─────────────────────────────────────────────
async def _react(bot: Client, message: Message, endpoint: str, caption_verb: str):
    """
    Generic reaction handler.
    endpoint  — waifu.pics SFW endpoint e.g. 'hug', 'slap'
    caption_verb — what the sender is doing e.g. 'hugged', 'slapped'
    """
    if not (message.reply_to_message and message.reply_to_message.from_user):
        return await message.edit("Reply to a user to react to them!")

    replied_user = message.reply_to_message.from_user
    user_link = f"[{replied_user.first_name}](tg://user?id={replied_user.id})"
    caption = f"**{caption_verb}** {user_link} 👉"

    URL = f"https://api.waifu.pics/sfw/{endpoint}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(URL) as resp:
                if resp.status != 200:
                    return await message.edit("❌ Could not fetch reaction GIF, try again!")
                result = await resp.json()
                url = result.get("url")

        await asyncio.gather(
            message.delete(),
            bot.send_video(
                GetChatID(message),
                url,
                reply_to_message_id=ReplyCheck(message),
                caption=caption,
            ),
        )
    except Exception as e:
        await message.edit(f"❌ Error: `{e}`")


# ─────────────────────────────────────────────
#  REACTION COMMANDS
# ─────────────────────────────────────────────

@on_message("bully",   allow_stan=True, Bad_user=True)
async def bully_cmd(bot, message):   await _react(bot, message, "bully",   "Bullied")

@on_message("cuddle",  allow_stan=True, Bad_user=True)
async def cuddle_cmd(bot, message):  await _react(bot, message, "cuddle",  "Cuddled")

@on_message("cry",     allow_stan=True, Bad_user=True)
async def cry_cmd(bot, message):     await _react(bot, message, "cry",     "Cried for")

@on_message("hug",     allow_stan=True, Bad_user=True)
async def hug_cmd(bot, message):     await _react(bot, message, "hug",     "Hugged")

@on_message("awoo",    allow_stan=True, Bad_user=True)
async def awoo_cmd(bot, message):    await _react(bot, message, "awoo",    "Awoo'd at")

@on_message("kiss",    allow_stan=True, Bad_user=True)
async def kiss_cmd(bot, message):    await _react(bot, message, "kiss",    "Kissed")

@on_message("lick",    allow_stan=True, Bad_user=True)
async def lick_cmd(bot, message):    await _react(bot, message, "lick",    "Licked")

@on_message("happy",   allow_stan=True, Bad_user=True)
async def happy_cmd(bot, message):   await _react(bot, message, "happy",   "Is happy with")

@on_message("kill",    allow_stan=True, Bad_user=True)
async def kill_cmd(bot, message):    await _react(bot, message, "kill",    "Killed")

@on_message("slap",    allow_stan=True, Bad_user=True)
async def slap_cmd(bot, message):    await _react(bot, message, "slap",    "Slapped")

@on_message("poke",    allow_stan=True, Bad_user=True)
async def poke_cmd(bot, message):    await _react(bot, message, "poke",    "Poked")

@on_message("dance",   allow_stan=True, Bad_user=True)
async def dance_cmd(bot, message):   await _react(bot, message, "dance",   "Danced with")

@on_message("cring",   allow_stan=True, Bad_user=True)
async def cringe_cmd(bot, message):  await _react(bot, message, "cringe",  "Cringed at")

# ── 3 New Reactions ──────────────────────────

@on_message("pat",     allow_stan=True, Bad_user=True)
async def pat_cmd(bot, message):     await _react(bot, message, "pat",     "Patted")

@on_message("wave",    allow_stan=True, Bad_user=True)
async def wave_cmd(bot, message):    await _react(bot, message, "wave",    "Waved at")

@on_message("punch",   allow_stan=True, Bad_user=True)
async def punch_cmd(bot, message):   await _react(bot, message, "punch",   "Punched")


# ─────────────────────────────────────────────
#  HELP MENU
# ─────────────────────────────────────────────
HelpMenu("reaction").add(
    "hug",    "<reply>", "Hug the replied user! 🤗",   "hug"
).add(
    "kiss",   "<reply>", "Kiss the replied user! 💋",  "kiss"
).add(
    "pat",    "<reply>", "Pat the replied user! 🤚",   "pat"
).add(
    "cuddle", "<reply>", "Cuddle the replied user! 🥰","cuddle"
).add(
    "slap",   "<reply>", "Slap the replied user! 👋",  "slap"
).add(
    "punch",  "<reply>", "Punch the replied user! 👊", "punch"
).add(
    "poke",   "<reply>", "Poke the replied user! 👉",  "poke"
).add(
    "bully",  "<reply>", "Bully the replied user! 😈", "bully"
).add(
    "kill",   "<reply>", "Kill the replied user! ☠️",  "kill"
).add(
    "lick",   "<reply>", "Lick the replied user! 👅",  "lick"
).add(
    "dance",  "<reply>", "Dance with the replied user! 💃", "dance"
).add(
    "wave",   "<reply>", "Wave at the replied user! 👋",    "wave"
).add(
    "cry",    "<reply>", "Cry for the replied user! 😭",    "cry"
).add(
    "happy",  "<reply>", "Share happiness with replied user! 😄", "happy"
).add(
    "awoo",   "<reply>", "Awoo at the replied user! 🐺",    "awoo"
).add(
    "cring",  "<reply>", "Cringe at the replied user! 😬",  "cring"
).info(
    "Reaction GIF Commands 🎭"
).done()
