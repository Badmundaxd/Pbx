import asyncio
from random import choice

from pyrogram import Client
from pyrogram.errors import FloodWait
from pyrogram.types import Message

from Pbxbot.bad.sukh import RAID, PBIRAID, OneWord, HIRAID, PORM, EMOJI
from . import HelpMenu, on_message, special, Bad


# ══════════════════════════════════════════════════════════════════
#  HELPER — user resolve + loop
# ══════════════════════════════════════════════════════════════════

async def _resolve_user(x: Client, e: Message, args: list):
    """Reply ya username/id se user resolve karo."""
    if e.reply_to_message and e.reply_to_message.from_user:
        return e.reply_to_message.from_user
    if len(args) >= 2:
        target = args[1]
        try:
            return await x.get_users(int(target) if target.isdigit() else target)
        except Exception:
            return None
    return None


async def _do_raid(x: Client, e: Message, pool: list, count: int, user):
    """
    Fast raid loop — FloodWait aave ta wait karke resume karo,
    crash na hoe.
    """
    await e.delete()
    sent = 0
    for _ in range(count):
        msg = f"[{user.first_name}](tg://user?id={user.id}) {choice(pool)}"
        while True:
            try:
                await x.send_message(e.chat.id, msg)
                sent += 1
                break
            except FloodWait as fw:
                await asyncio.sleep(fw.value)   # wait karke retry
            except Exception:
                return  # koi aur error — band karo
        await asyncio.sleep(0.05)  # min delay — fastest safe speed


def _parse_args(e: Message) -> list:
    return "".join(e.text.split(maxsplit=1)[1:]).split(" ", 2)


# ══════════════════════════════════════════════════════════════════
#  RAID COMMANDS
# ══════════════════════════════════════════════════════════════════

@on_message("raid", allow_stan=True, Bad_user=True, enable_log=True)
@Bad
@special
async def raid_cmd(x: Client, e: Message):
    args = _parse_args(e)
    if not args or not args[0].isdigit():
        return await e.reply_text("**Usage:** `.raid <count> <@user/reply>`")
    user = await _resolve_user(x, e, args)
    if not user:
        return await e.reply_text("**Usage:** `.raid <count> <@user/reply>`")
    await _do_raid(x, e, RAID, int(args[0]), user)


@on_message("pbiraid", allow_stan=True, Bad_user=True, enable_log=True)
@Bad
@special
async def pbiraid_cmd(x: Client, e: Message):
    args = _parse_args(e)
    if not args or not args[0].isdigit():
        return await e.reply_text("**Usage:** `.pbiraid <count> <@user/reply>`")
    user = await _resolve_user(x, e, args)
    if not user:
        return await e.reply_text("**Usage:** `.pbiraid <count> <@user/reply>`")
    await _do_raid(x, e, PBIRAID, int(args[0]), user)


@on_message("oneword", allow_stan=True, Bad_user=True, enable_log=True)
@Bad
@special
async def oneword_cmd(x: Client, e: Message):
    args = _parse_args(e)
    if not args or not args[0].isdigit():
        return await e.reply_text("**Usage:** `.oneword <count> <@user/reply>`")
    user = await _resolve_user(x, e, args)
    if not user:
        return await e.reply_text("**Usage:** `.oneword <count> <@user/reply>`")
    await _do_raid(x, e, OneWord, int(args[0]), user)


@on_message("hiraid", allow_stan=True, Bad_user=True, enable_log=True)
@Bad
@special
async def hiraid_cmd(x: Client, e: Message):
    args = _parse_args(e)
    if not args or not args[0].isdigit():
        return await e.reply_text("**Usage:** `.hiraid <count> <@user/reply>`")
    user = await _resolve_user(x, e, args)
    if not user:
        return await e.reply_text("**Usage:** `.hiraid <count> <@user/reply>`")
    await _do_raid(x, e, HIRAID, int(args[0]), user)


@on_message("imoji", allow_stan=True, Bad_user=True, enable_log=True)
@special
async def emoji_cmd(x: Client, e: Message):
    args = _parse_args(e)
    if not args or not args[0].isdigit():
        return await e.reply_text("**Usage:** `.imoji <count> <@user/reply>`")
    user = await _resolve_user(x, e, args)
    if not user:
        return await e.reply_text("**Usage:** `.imoji <count> <@user/reply>`")
    await _do_raid(x, e, EMOJI, int(args[0]), user)


# ══════════════════════════════════════════════════════════════════
#  PORNSPAM — video spam, FloodWait safe
# ══════════════════════════════════════════════════════════════════

@on_message("pornspam", allow_stan=True, Bad_user=True, enable_log=True)
@Bad
@special
async def pornspam_cmd(client: Client, message: Message):
    if len(message.command) < 2 or not message.command[1].isdigit():
        return await message.reply_text("**Usage:** `.pornspam <count>`")

    quantity = int(message.command[1])
    await message.delete()

    for _ in range(quantity):
        while True:
            try:
                await client.send_video(
                    chat_id=message.chat.id,
                    video=choice(PORM)
                )
                break
            except FloodWait as fw:
                await asyncio.sleep(fw.value)
            except Exception:
                return
        await asyncio.sleep(0.3)


# ══════════════════════════════════════════════════════════════════
#  HELP
# ══════════════════════════════════════════════════════════════════

HelpMenu("raid").add(
    "raid",     "<count> <@user/reply>", "Raid with messages.",      ".raid 10 @user"
).add(
    "pbiraid",  "<count> <@user/reply>", "Raid with Punjabi msgs.",  ".pbiraid 10 @user"
).add(
    "hiraid",   "<count> <@user/reply>", "Raid with Hindi msgs.",    ".hiraid 10 @user"
).add(
    "oneword",  "<count> <@user/reply>", "One word raid.",           ".oneword 10 @user"
).add(
    "imoji",    "<count> <@user/reply>", "Emoji raid.",              ".imoji 10 @user"
).add(
    "pornspam", "<count>",               "Video spam.",              ".pornspam 5"
).info("Raid & Spam Menu").done()
