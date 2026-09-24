import asyncio
import random

from pyrogram import Client
from pyrogram.errors.exceptions.flood_420 import FloodWait
from pyrogram.types import Message

from Pbxbot.bad.bad import edit_or_reply
from Pbxbot.bad.constants import MEMES
from . import HelpMenu, on_message, Bad, special

DEFAULTUSER = "PBX 4.0"

# ─────────────────────────────────────────────
#  CONSTANTS & DATA
# ─────────────────────────────────────────────
SLEEP = 0.1

NOBLE = [
    "╲╲╲┏━━┓╭━━━╮╱╱╱\n╲╲╲┗┓┏┛┃╭━╮┃╱╱╱\n╲╲╲╲┃┃┏┫┃╭┻┻┓╱╱\n╱╱╱┏╯╰╯┃╰┫┏━╯╱╱\n╱╱┏┻━┳┳┻━┫┗┓╱╱╱\n╱╱╰━┓┃┃╲┏┫┏┛╲╲╲\n╱╱╱╱┃╰╯╲┃┃┗━╮╲╲\n╱╱╱╱╰━━━╯╰━━┛╲╲",
    "┏━╮\n┃▔┃▂▂┏━━┓┏━┳━━━┓\n┃▂┣━━┻━╮┃┃▂┃▂┏━╯\n┃▔┃▔╭╮▔┃┃┃▔┃▔┗━┓\n┃▂┃▂╰╯▂┃┗╯▂┃▂▂▂┃\n┃▔┗━━━╮┃▔▔▔┃▔┏━╯\n┃▂▂▂▂▂┣╯▂▂▂┃▂┗━╮\n┗━━━━━┻━━━━┻━━━┛",
    "┏┓┏━┳━┳━┳━┓\n┃┗┫╋┣┓┃┏┫┻┫\n┗━┻━┛┗━┛┗━┛\n────YOU────",
    "╦──╔╗─╗╔─╔ ─\n║──║║─║║─╠ ─\n╚═─╚╝─╚╝─╚ ─\n╦─╦─╔╗─╦╦\n╚╦╝─║║─║║\n─╩──╚╝─╚╝",
    "░I░L░O░V░E░Y░O░U░",
    "╔ღ═╗╔╗\n╚╗╔╝║║ღ═╦╦╦═ღ\n╔╝╚╗ღ╚╣║║║║╠╣\n╚═ღ╝╚═╩═╩ღ╩═╝",
    "╔══╗....<3 \n╚╗╔╝..('\../') \n╔╝╚╗..( •.• ) \n╚══╝..(,,)(,,) \n╔╗╔═╦╦╦═╗ ╔╗╔╗ \n║╚╣║║║║╩╣ ║╚╝║ \n╚═╩═╩═╩═╝ ╚══╝",
]

R = "❤️"
W = "🤍"
heart_list = [
    W * 9, W * 2 + R * 2 + W + R * 2 + W * 2,
    W + R * 7 + W, W + R * 7 + W, W + R * 7 + W,
    W * 2 + R * 5 + W * 2, W * 3 + R * 3 + W * 3,
    W * 4 + R + W * 4, W * 9,
]
joined_heart = "\n".join(heart_list)
heartlet_len = joined_heart.count(R)


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
async def _safe_edit(message, text: str):
    try:
        await message.edit(text)
    except FloodWait as fl:
        await asyncio.sleep(fl.value)


async def _animate(message, frames: list, interval: float = 0.3):
    for frame in frames:
        await _safe_edit(message, frame)
        await asyncio.sleep(interval)


async def phase1(message):
    BIG_SCROLL = "🧡💛💚💙💜🖤🤎"
    await _safe_edit(message, joined_heart)
    for heart in BIG_SCROLL:
        await _safe_edit(message, joined_heart.replace(R, heart))
        await asyncio.sleep(SLEEP)


# ─────────────────────────────────────────────
#  COMMANDS
# ─────────────────────────────────────────────

@on_message("love", allow_stan=True, Bad_user=True)
async def love_cmd(client: Client, message: Message):
    await phase1(message)
    await asyncio.sleep(SLEEP * 3)
    for text in ["❤️ I", "❤️ I Love", "❤️ I Love You", "❤️ I Love You <3"]:
        await message.edit(text)
        await asyncio.sleep(0.5)


@on_message("bad", allow_stan=True, Bad_user=True)
async def bad_cmd(client: Client, message: Message):
    await phase1(message)
    await asyncio.sleep(SLEEP * 3)
    for text in ["❤️ ᴍʏ", "💝 ᴍʏ ᴄᴜᴛᴇ", "💞 ᴍʏ ᴄᴜᴛᴇ ᴏᴡɴᴇʀ"]:
        await message.edit(text)
        await asyncio.sleep(0.5)
    await asyncio.sleep(3)
    await message.edit("[⎯꯭̽🇨🇦꯭꯭ ⃪В꯭α꯭∂ ꯭м꯭υ꯭η∂꯭α_꯭آآ⎯꯭ ꯭̽🌸](https://t.me/ll_BAD_MUNDA_ll)")


@on_message("rain", allow_stan=True, Bad_user=True)
async def rain_cmd(client: Client, message: Message):
    await phase1(message)
    await asyncio.sleep(SLEEP * 3)
    await _animate(message, ["🌬", "☁️", "🌩", "🌨", "🌧", "🌦", "🌨🌩🌦🌥⛅🌤"], interval=0.5)


@on_message("shizu", allow_stan=True, Bad_user=True)
async def shizu_cmd(client: Client, message: Message):
    await phase1(message)
    await asyncio.sleep(SLEEP * 3)
    frames = [
        "😘😘ʙᴀʙʏ sᴜɴᴏ ɴᴀ😘😘", "😍ᴍᴇʀᴀ ʙᴀᴄʜᴀ 😍",
        "😍ʙᴀʙʏ ɪ ʟᴏᴠᴇ ʟᴏᴠᴇ ʟᴏᴠᴇ ʏᴏᴜ🥰", "😘ʙᴀʙʏ ɪ ᴍɪss ʏᴏᴜ sᴏ ᴍᴜᴄʜ🙁",
        "🫣ᴛᴜ ᴍᴇʀɪ ᴀ ᴊᴀᴀɴ ᴍᴇᴛɪ 🤗", "💋ʙᴀʙʏ ɪ ᴋɪss ʏᴏᴜ 🥰",
        "🙈sʜɪᴢᴜ ᴊᴀᴀɴ ɪ ʟᴏᴠᴇ ʏᴏᴜ ɪ ᴍɪss ʏᴏᴜ ɪ ᴋɪss ʏᴏᴜ💫🥰❤️",
    ]
    await _animate(message, frames, interval=0.5)


@on_message("loveu", allow_stan=True, Bad_user=True)
async def loveu_cmd(client: Client, message: Message):
    await edit_or_reply(message, random.choice(NOBLE))


@on_message("hmm", allow_stan=True, Bad_user=True)
async def hmm_cmd(client: Client, message: Message):
    await edit_or_reply(
        message,
        "┈┈╱▔▔▔▔▔╲┈┈┈HM┈HM\n┈╱┈┈╱▔╲╲╲▏┈┈┈HMMM\n╱┈┈╱━╱▔▔▔▔▔╲━╮┈┈\n▏┈▕┃▕╱▔╲╱▔╲▕╮┃┈┈\n▏┈▕╰━▏▊▕▕▋▕▕━╯┈┈\n╲┈┈╲╱▔╭╮▔▔┳╲╲┈┈┈\n┈╲┈┈▏╭━━━━╯▕▕┈┈┈\n┈┈╲┈╲▂▂▂▂▂▂╱╱┈┈┈",
    )


@on_message("ahh", allow_stan=True, Bad_user=True)
async def ahh_cmd(client: Client, message: Message):
    frames = ["ahh", "aahh", "aahhh", "aahhhh", "aahhhhh", "aahhhhhh", "aahhhhhhh", "aaahhhhhhhh"]
    mg = await edit_or_reply(message, frames[0])
    for f in frames[1:]:
        await asyncio.sleep(0.2)
        await mg.edit(f)


@on_message("shoot", allow_stan=True, Bad_user=True)
async def shoot_cmd(client: Client, message: Message):
    await edit_or_reply(
        message,
        "░▐█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█▄\n░███████████████████████....⁍\n░▓▓▓▓▓▓▓▓▓▓▓▓██▓▓▓▓▓▓▓▓◤\n╬▀░▐▓▓▓▓▓▓▌▀█░░░█▀░\n▒░░▓▓▓▓▓▓█▄▄▄▄▄█▀╬░\n░░█▓▓▓▓▓▌░▒▒▒▒▒▒▒▒▒\n░▐█▓▓▓▓▓░░▒▒▒▒▒▒▒▒▒\n░▐██████▌╬░▒▒▒▒▒▒▒▒\n",
    )


@on_message("brain", allow_stan=True, Bad_user=True)
async def brain_cmd(client: Client, message: Message):
    frames = [
        "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n🧠         <(^_^ <)🗑",
        "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n🧠       <(^_^ <)  🗑",
        "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n🧠     <(^_^ <)    🗑",
        "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n🧠   <(^_^ <)      🗑",
        "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n🧠 <(^_^ <)        🗑",
        "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n🧠<(^_^ <)         🗑",
        "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n(> ^_^)>🧠         🗑",
        "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n  (> ^_^)>🧠       🗑",
        "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n    (> ^_^)>🧠     🗑",
        "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n      (> ^_^)>🧠   🗑",
        "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n        (> ^_^)>🧠 🗑",
        "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n          (> ^_^)>🧠🗑",
        "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n           (> ^_^)>🗑",
        "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n           <(^_^ <)🗑",
    ]
    await message.edit("brain")
    await _animate(message, frames, interval=1)


@on_message("sex", allow_stan=True, Bad_user=True)
async def sex_cmd(client: Client, message: Message):
    frames = [
        "1 ❤️ love story",
        "  😐             😕 \n/👕\         <👗\ \n 👖               /|",
        "  😉          😳 \n/👕\       /👗\ \n  👖            /|",
        "  😚            😒 \n/👕\         <👗> \n  👖             /|",
        "  😍         ☺️ \n/👕\      /👗\ \n  👖          /|",
        "  😍          😍 \n/👕\       /👗\ \n  👖           /|",
        "  😘   😊 \n /👕\/👗\ \n   👖   /|",
        " 😳  😁 \n /|\ /👙\ \n /     / |",
        "😈    /😰\ \n<|\      👙 \n /🍆    / |",
        "😅 \n/(),✊😮 \n /\         _/\\/|",
        "😎 \n/\\_,__😫 \n  //    //       \\",
        "😖 \n/\\_,💦_😋  \n  //         //        \\",
        "  😭      ☺️ \n  /|\   /(👶)\ \n  /!\   / \ ",
        "Abee aur kitna dekhoge be besharmi ki bhi hadd hoti hai..,The End 😂...",
    ]
    await message.edit("sex")
    await _animate(message, frames, interval=1)


@on_message("bomb", allow_stan=True, Bad_user=True)
async def bomb_cmd(client: Client, message: Message):
    frames = [
        "▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n",
        "💣💣💣💣 \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n",
        "▪️▪️▪️▪️ \n💣💣💣💣 \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n",
        "▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n💣💣💣💣 \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n",
        "▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n💣💣💣💣 \n▪️▪️▪️▪️ \n",
        "▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n💣💣💣💣 \n",
        "▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n💥💥💥💥 \n",
        "▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n💥💥💥💥 \n💥💥💥💥 \n",
        "▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n😵😵😵😵 \n",
        "`RIP PLOXXX......`",
    ]
    await _animate(message, frames, interval=0.5)


@on_message("call", allow_stan=True, Bad_user=True)
async def call_cmd(client: Client, message: Message):
    frames = [
        "`Connecting To Telegram Headquarters...`",
        "`Call Connected.`",
        "`Telegram: Hello This is Telegram HQ. Who is this?`",
        f"`Me: Yo this is` {DEFAULTUSER} ,`Please Connect me to my lil bro, Pavel Durov`",
        "`User Authorised.`",
        f"`Calling {DEFAULTUSER} At +14382366553`",
        "`Private Call Connected...`",
        "`Me: Hello Sir, Please Ban This Telegram Account.`",
        "`Saitama : May I Know Who Is This?`",
        f"`Me: Yo Brah, I Am` {DEFAULTUSER}",
        "`Saitama : OMG!!! Long time no see, Wassup!\nI'll Make Sure That Guy Account Will Get Blocked Within 24Hrs.`",
        "`Me: Thanks, See You Later Brah.`",
        "`Saitama : Please Don't Thank Brah, Telegram Is Ours. Just Gimme A Call When You Become Free.`",
        "`Me: Is There Any Issue/Emergency???`",
        "`Saitama : Yes Sir, There Is A Bug In Telegram v69.6.9.\nI Am Not Able To Fix It. If Possible, Please Help Fix The Bug.`",
        "`Me: Send Me The App On My Telegram Account, I Will Fix The Bug & Send You.`",
        "`Saitama : Sure Sir\nTC Bye Bye :)`",
        "`Private Call Disconnected.`",
    ]
    await message.edit("Calling Pavel Durov (CEO of Telegram)......")
    await _animate(message, frames, interval=3)


@on_message("theart", allow_stan=True, Bad_user=True)
async def theart_cmd(client: Client, message: Message):
    hearts = ["❤️","🧡","💛","💚","💙","💜","🖤","💘","💝","❤️","🧡","💛","💝","💜"]
    await _animate(message, hearts, interval=0.5)


@on_message("wtf", allow_stan=True, Bad_user=True)
async def wtf_cmd(client: Client, message: Message):
    frames = [
        "What", "What The", "What The F", "What The F Brah",
        "[𝗪𝗵𝗮𝘁 𝗧𝗵𝗲 𝗙 𝗕𝗿𝗮𝗵](https://telegra.ph//file/f3b760e4a99340d331f9b.jpg)",
    ]
    await message.edit("wtf")
    await _animate(message, frames, interval=0.8)


@on_message("ding", allow_stan=True, Bad_user=True)
async def ding_cmd(client: Client, message: Message):
    frames = [
        "🔴⬛⬛⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜",
        "⬜⬜⬛⬜⬜\n⬜⬛⬜⬜⬜\n🔴⬜⬜⬜⬜",
        "⬜⬜⬛⬜⬜\n⬜⬜⬛⬜⬜\n⬜⬜🔴⬜⬜",
        "⬜⬜⬛⬜⬜\n⬜⬜⬜⬛⬜\n⬜⬜⬜⬜🔴",
        "⬜⬜⬛⬛🔴\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜",
        "⬜⬜⬛⬜⬜\n⬜⬜⬜⬛⬜\n⬜⬜⬜⬜🔴",
        "⬜⬜⬛⬜⬜\n⬜⬜⬛⬜⬜\n⬜⬜🔴⬜⬜",
        "⬜⬜⬛⬜⬜\n⬜⬛⬜⬜⬜\n🔴⬜⬜⬜⬜",
        "🔴⬛⬛⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜",
        "⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜\n⬜  [PBX IS BEST](https://pbx4-0.vercel.app/) ⬜\n⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜",
    ]
    await message.edit("ding..dong..ding..dong ...")
    await asyncio.sleep(4)
    for _ in range(3):
        await _animate(message, frames, interval=0.3)


@on_message("hypo", allow_stan=True, Bad_user=True)
async def hypo_cmd(client: Client, message: Message):
    frames = [
        "⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜",
        "⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬛⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜",
        "⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬛⬛⬛⬜⬜\n⬜⬜⬛⬜⬛⬜⬜\n⬜⬜⬛⬛⬛⬜⬜\n⬜⬜⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜⬜⬜",
        "⬜⬜⬜⬜⬜⬜⬜\n⬜⬛⬛⬛⬛⬛⬜\n⬜⬛⬜⬜⬜⬛⬜\n⬜⬛⬜⬜⬜⬛⬜\n⬜⬛⬜⬜⬜⬛⬜\n⬜⬛⬛⬛⬛⬛⬜\n⬜⬜⬜⬜⬜⬜⬜",
        "⬛⬛⬛⬛⬛⬛⬛\n⬛⬜⬜⬜⬜⬜⬛\n⬛⬜⬜⬜⬜⬜⬛\n⬛⬜⬜⬜⬜⬜⬛\n⬛⬜⬜⬜⬜⬜⬛\n⬛⬜⬜⬜⬜⬜⬛\n⬛⬛⬛⬛⬛⬛⬛",
        "⬛⬜⬛⬜⬛⬜⬛⬜\n⬜⬛⬜⬛⬜⬛⬜⬛\n⬛⬜⬛⬜⬛⬜⬛⬜\n⬜⬛⬜⬛⬜⬛⬜⬛\n⬛⬜⬛⬜⬛⬜⬛⬜\n⬜⬛⬜⬛⬜⬛⬜⬛\n⬛⬜⬛⬜⬛⬜⬛⬜",
        "⬜⬛⬜⬛⬜⬛⬜⬛\n⬛⬜⬛⬜⬛⬜⬛⬜\n⬜⬛⬜⬛⬜⬛⬜⬛\n⬛⬜⬛⬜⬛⬜⬛⬜\n⬜⬛⬜⬛⬜⬛⬜⬛\n⬛⬜⬛⬜⬛⬜⬛⬜\n⬜⬛⬜⬛⬜⬛⬜⬛",
        "⬜⬜⬜⬜⬜⬜⬜\n⬜⬛⬛⬛⬛⬛⬜\n⬜⬛⬜⬜⬜⬛⬜\n⬜⬛⬜⬛⬜⬛⬜\n⬜⬛⬜⬜⬜⬛⬜\n⬜⬛⬛⬛⬛⬛⬜\n⬜⬜⬜⬜⬜⬜⬜",
        "⬛⬛⬛⬛⬛⬛⬛\n⬛⬜⬜⬜⬜⬜⬛\n⬛⬜⬛⬛⬛⬜⬛\n⬛⬜⬛⬜⬛⬜⬛\n⬛⬜⬛⬛⬛⬜⬛\n⬛⬜⬜⬜⬜⬜⬛\n⬛⬛⬛⬛⬛⬛⬛",
        "⬜⬜⬜⬜⬜⬜⬜\n⬜⬛⬛⬛⬛⬛⬜\n⬜⬛⬜⬜⬜⬛⬜\n⬜⬛⬜⬛⬜⬛⬜\n⬜⬛⬜⬜⬜⬛⬜\n⬜⬛⬛⬛⬛⬛⬜\n⬜⬜⬜⬜⬜⬜⬜",
        "⬛⬛⬛⬛⬛\n⬛⬜⬜⬜⬛\n⬛⬜⬛⬜⬛\n⬛⬜⬜⬜⬛\n⬛⬛⬛⬛⬛",
        "⬜⬜⬜\n⬜⬛⬜\n⬜⬜⬜",
        "[👉🔴👈]",
    ]
    await message.edit("hypo....")
    await _animate(message, frames, interval=0.3)


@on_message("gangstar", allow_stan=True, Bad_user=True)
async def gangstar_cmd(client: Client, message: Message):
    frames = ["EVERyBOdy", "iZ", "GangSTur", "UNtIL ", "I", "ArRivE", "🔥🔥🔥", "EVERyBOdy iZ GangSTur UNtIL I ArRivE 🔥🔥🔥"]
    await _animate(message, frames, interval=0.3)


@on_message("charging", allow_stan=True, Bad_user=True)
async def charging_cmd(client: Client, message: Message):
    txt = "Tesla Wireless Charging (beta) Started...\nDevice Detected: Nokia 1100\nBattery Percentage: "
    for k in range(10, 101, 10):
        await message.edit(f"`{txt}{k}%`")
        await asyncio.sleep(1)
    await asyncio.sleep(1)
    await message.edit(
        "`Tesla Wireless Charging (beta) Completed...\nDevice Detected: Nokia 1100\nBattery Percentage:` [100%](https://telegra.ph/file/a45aa7450c8eefed599d9.mp4)",
        link_preview=True,
    )


@on_message("muth", allow_stan=True, Bad_user=True)
async def muth_cmd(client: Client, message: Message):
    frames = [
        "8✊===D", "8=✊==D", "8==✊=D", "8===✊D",
        "8==✊=D", "8=✊==D", "8✊===D", "8=✊==D",
        "8==✊=D", "8===✊D", "8==✊=D", "8=✊==D",
        "8✊===D", "8=✊==D", "8==✊=D", "8===✊D",
        "8==✊=D", "8=✊==D",
        "8===✊D💦", "8==✊=D💦💦", "8=✊==D💦💦💦",
        "8✊===D💦💦💦💦", "8===✊D💦💦💦💦💦",
        "8==✊=D💦💦💦💦💦💦", "8=✊==D💦💦💦💦💦💦💦",
        "8✊===D💦💦💦💦💦💦??💦", "8===✊D💦💦💦💦💦💦💦💦💦",
        "8==✊=D💦💦💦💦💦💦💦💦💦💦",
        "8=✊==D That's why it's over?", "😭😭😭😭",
    ]
    e = await edit_or_reply(message, frames[0])
    for f in frames[1:]:
        await e.edit(f)


@on_message("fuck", allow_stan=True, Bad_user=True)
@Bad
@special
async def fuck_cmd(client: Client, message: Message):
    lines = [
        ".                       /¯ )",
        ".                       /¯ )\n                      /¯  /",
        ".                       /¯ )\n                      /¯  /\n                    /    /",
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸",
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ ",
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')",
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')\n         \\                        /",
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')\n         \\                        /\n          \\                _.•´",
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')\n         \\                        /\n          \\                _.•´\n            \\              (",
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')\n         \\                        /\n          \\                _.•´\n            \\              (\n              \\  ",
    ]
    e = await edit_or_reply(message, lines[0])
    for line in lines[1:]:
        await e.edit(line)


@on_message("hack", allow_stan=True, Bad_user=True)
async def hack_cmd(client: Client, message: Message):
    steps = [
        ("Looking for WhatsApp databases in targeted person...", 2),
        (" User online: True\nTelegram access: True\nRead Storage: True ", 2),
        ("Hacking... 0%\n[░░░░░░░░░░░░░░░░░░░░]\n`Looking for WhatsApp...`\nETA: 0m, 20s", 2),
        ("Hacking... 11.07%\n[██░░░░░░░░░░░░░░░░░░]\n`Looking for WhatsApp...`\nETA: 0m, 18s", 2),
        ("Hacking... 20.63%\n[███░░░░░░░░░░░░░░░░░]\n`Found folder C:/WhatsApp`\nETA: 0m, 16s", 2),
        ("Hacking... 34.42%\n[█████░░░░░░░░░░░░░░░]\n`Found folder C:/WhatsApp`\nETA: 0m, 14s", 2),
        ("Hacking... 42.17%\n[███████░░░░░░░░░░░░░]\n`Searching for databases`\nETA: 0m, 12s", 2),
        ("Hacking... 55.30%\n[█████████░░░░░░░░░░░]\n`Found msgstore.db.crypt12`\nETA: 0m, 10s", 2),
        ("Hacking... 64.86%\n[███████████░░░░░░░░░]\n`Found msgstore.db.crypt12`\nETA: 0m, 08s", 2),
        ("Hacking... 74.02%\n[█████████████░░░░░░░]\n`Trying to Decrypt...`\nETA: 0m, 06s", 2),
        ("Hacking... 86.21%\n[███████████████░░░░░]\n`Trying to Decrypt...`\nETA: 0m, 04s", 2),
        ("Hacking... 93.50%\n[█████████████████░░░]\n`Decryption successful!`\nETA: 0m, 02s", 2),
        ("Hacking... 100%\n[████████████████████]\n`Scanning file...`\nETA: 0m, 00s", 2),
        ("Hacking complete!\nUploading file...", 2),
        ("Targeted Account Hacked...!\n\n ✅ File has been successfully uploaded to my server.\nWhatsApp Database:\n`./DOWNLOADS/msgstore.db.crypt12`", 0),
    ]
    for text, delay in steps:
        await message.edit_text(text)
        if delay:
            await asyncio.sleep(delay)


@on_message("dino", allow_stan=True, Bad_user=True)
async def dino_cmd(client: Client, message: Message):
    typew = await edit_or_reply(message, "`DIN DINNN.....`")
    await asyncio.sleep(1)
    positions = [
        "`🏃                        🦖`", "`🏃                       🦖`", "`🏃                      🦖`",
        "`🏃                     🦖`", "`🏃   Larius         🦖`", "`🏃                   🦖`",
        "`🏃                  🦖`", "`🏃                 🦖`", "`🏃                🦖`",
        "`🏃               🦖`", "`🏃              🦖`", "`🏃             🦖`",
        "`🏃            🦖`", "`🏃           🦖`", "`🏃WORGH!   🦖`",
        "`🏃           🦖`", "`🏃            🦖`", "`🏃             🦖`",
        "`🏃              🦖`", "`🏃               🦖`", "`🏃                🦖`",
        "`🏃                 🦖`", "`🏃                  🦖`", "`🏃                   🦖`",
        "`🏃                    🦖`", "`🏃                     🦖`", "`🏃  Huh-Huh           🦖`",
        "`🏃                   🦖`", "`🏃                  🦖`", "`🏃                 🦖`",
        "`🏃                🦖`", "`🏃               🦖`", "`🏃              🦖`",
        "`🏃             🦖`", "`🏃            🦖`", "`🏃           🦖`",
        "`🏃          🦖`", "`🏃         🦖`",
    ]
    for p in positions:
        await typew.edit(p)
    await typew.edit("`HE'S GETTING CLOSER!!!`")
    await asyncio.sleep(1)
    for p in ["`🏃       🦖`", "`🏃      🦖`", "`🏃     🦖`", "`🏃    🦖`"]:
        await typew.edit(p)
    await typew.edit("`Just give up`")
    await asyncio.sleep(1)
    await typew.edit("`🧎🦖`")
    await asyncio.sleep(2)
    await typew.edit("`-ENDED-`")


@on_message("cobra", allow_stan=True, Bad_user=True)
async def cobra_cmd(client: Client, message: Message):
    await edit_or_reply(
        message,
        "░░░░▓\n░░░▓▓\n░░█▓▓█\n░██▓▓██\n░░██▓▓██\n░░░██▓▓██\n░░░░██▓▓██\n░░░░░██▓▓██\n"
        "░░░░██▓▓██\n░░░██▓▓██\n░░██▓▓██\n░██▓▓██\n░░██▓▓██\n░░░██▓▓██\n░░░░██▓▓██\n"
        "░░░░░██▓▓██\n░░░░██▓▓██\n░░░██▓▓██\n░░██▓▓██\n░██▓▓██\n"
        "░░░░░░███▓▓███████\n░░░░████▓▓████████\n░░░█████▓▓█████████\n"
        "░░░█████░░░█████●███\n░░████░░░░░░░███████\n░░███░░░░░░░░░██████\n"
        "░░██░░░░░░░░░░░████\n░░░░░░░░░░░░░░░░███\n░░░░░░░░░░░░░░░░░░░\n",
    )


@on_message("helicopter", allow_stan=True, Bad_user=True)
async def helicopter_cmd(client: Client, message: Message):
    await edit_or_reply(
        message,
        "▬▬▬.◙.▬▬▬ \n═▂▄▄▓▄▄▂ \n◢◤ █▀▀████▄▄▄▄◢◤ \n█▄ █ █▄ ███▀▀▀▀▀▀▀╬ \n◥█████◤ \n══╩══╩══ \n╬═╬ \n╬═╬ \n╬═╬ \n╬═╬ \n╬═╬ \n╬═╬ \n╬═╬ Hello Everything :) \n╬═╬☻/ \n╬═╬/▌ \n╬═╬/ \\ \n",
    )


@on_message("gf", allow_stan=True, Bad_user=True)
async def gf_cmd(client: Client, message: Message):
    await edit_or_reply(
        message,
        "_/﹋\\_\n(҂`_´)\n<,︻╦╤─ ҉\n_/﹋\\_\n**Do you want to be my girlfriend??!**",
    )


@on_message("drugs", allow_stan=True, Bad_user=True)
async def drugs_cmd(client: Client, message: Message):
    await edit_or_reply(
        message,
        "`Drugs Everything...`          \n　　　　　|\n　　　　　| \n　　　　　| \n　　　　　| \n　　　　　| \n"
        "　　　　　| \n　　　　　| \n　　　　　| \n　／￣￣＼| \n＜ ´･ 　　 |＼ \n　|　３　 | 丶＼ \n"
        "＜ 、･　　|　　＼ \n　＼＿＿／∪ _ ∪) \n　　　　　 Ｕ Ｕ\n",
    )


@on_message("run", allow_stan=True, Bad_user=True)
async def run_cmd(client: Client, message: Message):
    await edit_or_reply(
        message,
        "────██──────▀▀▀██\n──▄▀█▄▄▄─────▄▀█▄▄▄\n▄▀──█▄▄──────█─█▄▄\n─▄▄▄▀──▀▄───▄▄▄▀──▀▄\n─▀───────▀▀─▀───────▀▀\n`Awkwokwokwok..`",
    )


@on_message("thumb", allow_stan=True, Bad_user=True)
async def thumb_cmd(client: Client, message: Message):
    await edit_or_reply(
        message,
        "‡‡‡‡‡‡‡‡‡‡‡‡▄▄▄▄\n‡‡‡‡‡‡‡‡‡‡‡█‡‡‡‡█\n‡‡‡‡‡‡‡‡‡‡‡█‡‡‡‡█\n"
        "‡‡‡‡‡‡‡‡‡‡█‡‡‡‡‡█\n‡‡‡‡‡‡‡‡‡█‡‡‡‡‡‡█\n██████▄▄█‡‡‡‡‡‡████████▄\n"
        "▓▓▓▓▓▓█‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡█\n▓▓▓▓▓▓█‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡█\n"
        "▓▓▓▓▓▓█‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡█\n▓▓▓▓▓▓█‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡█\n"
        "▓▓▓▓▓▓█‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡█\n▓▓▓▓▓▓█████‡‡‡‡‡‡‡‡‡‡‡‡██\n█████‡‡‡‡‡‡‡██████████\n",
    )


@on_message("tank", allow_stan=True, Bad_user=True)
async def tank_cmd(client: Client, message: Message):
    await edit_or_reply(
        message,
        "█۞███████]▄▄▄▄▄▄▄▄▄▄▃ \n▂▄▅█████████▅▄▃▂…\n[███████████████████]\n◥⊙▲⊙▲⊙▲⊙▲⊙▲⊙▲⊙◤\n",
    )


@on_message("cat", allow_stan=True, Bad_user=True)
async def cat_cmd(client: Client, message: Message):
    await edit_or_reply(
        message,
        "┈┈┏━╮╭━┓┈╭━━━━╮\n┈┈┃┏┗┛┓┃╭┫cat ┃\n┈┈╰┓▋▋┏╯╯╰━━━━╯\n"
        "┈╭━┻╮╲┗━━━━╮╭╮┈\n┈┃▎▎┃╲╲╲╲╲╲┣━╯┈\n┈╰━┳┻▅╯╲╲╲╲┃┈┈┈\n"
        "┈┈┈╰━┳┓┏┳┓┏╯┈┈┈\n┈┈┈┈┈┗┻┛┗┻┛┈┈┈┈\n",
    )


@on_message("pat", allow_stan=True, Bad_user=True)
async def pat_cmd(client: Client, message: Message):
    await edit_or_reply(
        message,
        "╥━━━━━━━━╭━━╮━━┳\n╢╭╮╭━━━━━┫┃▋▋━▅┣\n╢┃╰┫┈┈┈┈┈┃┃┈┈╰┫┣\n"
        "╢╰━┫┈┈┈┈┈╰╯╰┳━╯┣\n╢┊┊┃┏┳┳━━┓┏┳┫┊┊┣\n╨━━┗┛┗┛━━┗┛┗┛━━┻\n",
    )


@on_message("nolove", allow_stan=True, Bad_user=True)
async def nolove_cmd(client: Client, message: Message):
    typew = await edit_or_reply(
        message, "`(\\_/)``\n(●_●)``\n />💖 *This is for you`"
    )
    await asyncio.sleep(2)
    await typew.edit("`(\\_/)``\n(●_●)``\n💖<\\  *tap IB OO that one`")


@on_message("scam", allow_stan=True, Bad_user=True)
async def scam_cmd(client: Client, message: Message):
    typew = await edit_or_reply(message, "`Activates Witchcraft Commands Online....`")
    await asyncio.sleep(2)
    await typew.edit("`Search for This Person's Name...`")
    await asyncio.sleep(1)
    await typew.edit("`Online Witchcraft Performed Immediately`")
    await asyncio.sleep(1)

    # Progress bar — clean loop instead of 300 hardcoded lines
    blocks = ["▎","▍","▌","▊","▉","█","█▎","█▍","█▌","█▊","█▉","██","██▎","██▍","██▌","██▊","██▉","███","███▎","███▍","███▌","███▊","███▉","████","████▎","████▍","████▌","████▊","████▉","█████","█████▎","█████▍","█████▌","█████▊","█████▉","██████","██████▎","██████▍","██████▌","██████▊","██████▉","███████","███████▎","███████▍","███████▌","███████▊","███████▉","████████","████████▎","████████▍","████████▌","████████▊","████████▉","█████████","█████████▎","█████████▍","█████████▌","█████████▊","█████████▉","██████████","██████████▎","██████████▍","██████████▌","██████████▊","██████████▉","███████████","███████████▎","███████████▍","███████████▌","███████████▊","███████████▉","████████████","████████████▎","████████████▍","████████████▌","████████████▊","████████████▉","█████████████","█████████████▎","█████████████▍","█████████████▌","█████████████▊","█████████████▉","██████████████","██████████████▎","██████████████▍","██████████████▌","██████████████▊","██████████████▉","███████████████","███████████████▎","███████████████▍","███████████████▌","███████████████▊","███████████████▉","████████████████","████████████████▎","████████████████▍","████████████████▌","████████████████▌"]

    await typew.edit("0%")
    for i, bar in enumerate(blocks, start=1):
        await typew.edit(f"{i}%   {bar}")
        await asyncio.sleep(0.03)

    await asyncio.sleep(1)
    await typew.edit("**Target Successfully Scammed Online 🥴**")


@on_message("ror", allow_stan=True, Bad_user=True)
async def ror_cmd(client: Client, message: Message):
    await phase1(message)
    await asyncio.sleep(SLEEP * 1.5)
    await _animate(message, ["Rooor", "Rooor Aahh", "Rooor Aahh Aahh", "Rooor Aahh Aahh Aahh"], interval=1)


# ─────────────────────────────────────────────
#  HELP MENU
# ─────────────────────────────────────────────
HelpMenu("animation").add(
    "love", None, "I Love You heart animation ❤️"
).add("bad", None, "Bad Munda owner message 😎"
).add("rain", None, "Rain weather animation 🌧"
).add("shizu", None, "Shizu love message 💕"
).add("loveu", None, "Random love art quote 💌"
).add("hmm", None, "Hmm ASCII art 🤔"
).add("ahh", None, "Ahh growing text 😱"
).add("shoot", None, "Gun ASCII art 🔫"
).add("brain", None, "Brain trash animation 🧠"
).add("sex", None, "Love story animation 😏"
).add("bomb", None, "Bomb drop effect 💣"
).add("call", None, "Calling Pavel Durov effect 📞"
).add("theart", None, "Rainbow hearts animation 💜"
).add("wtf", None, "WTF reaction 😳"
).add("ding", None, "Ding dong ball animation 🔴"
).add("hypo", None, "Hypnotic grid animation 🌀"
).add("gangstar", None, "Everybody is gangstar entry 🔥"
).add("charging", None, "Fake wireless charging animation ⚡"
).add("muth", None, "Muth reaction animation 💦"
).add("fuck", None, "ASCII middle finger art 🖕"
).add("hack", None, "Fake WhatsApp hacking animation 💻"
).add("dino", None, "Dinosaur chase animation 🦖"
).add("cobra", None, "Cobra snake ASCII art 🐍"
).add("helicopter", None, "Helicopter ASCII art 🚁"
).add("gf", None, "Girlfriend proposal message 💘"
).add("drugs", None, "Drugs ASCII art 🐱"
).add("run", None, "Running man ASCII art 🏃"
).add("thumb", None, "Thumbs up ASCII art 👍"
).add("tank", None, "Tank ASCII art 🪖"
).add("cat", None, "Cat ASCII art 🐱"
).add("pat", None, "Pat ASCII art 🤚"
).add("nolove", None, "No love bunny animation 💔"
).add("scam", None, "Online scam progress bar 🥴"
).add("ror", None, "Roar animation 🦁"
).info("Fun / Animation / Art Commands").done()
