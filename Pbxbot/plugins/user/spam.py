import asyncio

from pyrogram import Client
from pyrogram.errors import FloodWait
from pyrogram.types import Message

from . import HelpMenu, Symbols, Pbxbot, on_message, special

spamTask = {}


# ══════════════════════════════════════════════════════════════════
#  CORE SPAM LOOP — FloodWait safe, fast
# ══════════════════════════════════════════════════════════════════

async def spam_text(
    client: Client,
    chat_id: int,
    to_spam: str,
    count: int,
    reply_to: int,
    delay: float,
    copy_id: int,
    event: asyncio.Event,
):
    for _ in range(count):
        if event.is_set():
            break

        while True:
            try:
                if copy_id:
                    await client.copy_message(
                        chat_id, chat_id, copy_id,
                        reply_to_message_id=reply_to
                    )
                else:
                    await client.send_message(
                        chat_id,
                        to_spam,
                        disable_web_page_preview=True,
                        reply_to_message_id=reply_to,
                    )
                break  # success — agle iteration pe jao
            except FloodWait as fw:
                # Flood aaya — wait karke retry, stop nahi
                await asyncio.sleep(fw.value)
            except Exception:
                event.set()
                break

        if delay:
            await asyncio.sleep(delay)

    # Cleanup
    try:
        event.set()
        task = spamTask.get(chat_id)
        if task:
            task.remove(event)
    except Exception:
        pass

    await Pbxbot.check_and_log(
        "spam",
        f"**Count:** `{count}`\n**Chat:** `{chat_id}`\n**Client:** {client.me.first_name}",
    )


def _register_task(chat_id: int, event: asyncio.Event):
    if spamTask.get(chat_id):
        spamTask[chat_id].append(event)
    else:
        spamTask[chat_id] = [event]


# ══════════════════════════════════════════════════════════════════
#  COMMANDS
# ══════════════════════════════════════════════════════════════════

@on_message("spam", allow_stan=True, Bad_user=True, enable_log=True)
@special
async def spamMessage(client: Client, message: Message):
    if len(message.command) < 3:
        return await Pbxbot.delete(message, "**Usage:** `.spam <count> <message>`")
    try:
        count = int(message.command[1])
    except ValueError:
        return await Pbxbot.delete(message, "Give me a valid number.")

    reply_to = message.reply_to_message.id if message.reply_to_message else None
    to_spam  = message.text.split(" ", 2)[2].strip()
    event    = asyncio.Event()

    _register_task(message.chat.id, event)
    await message.delete()
    await asyncio.create_task(
        spam_text(client, message.chat.id, to_spam, count, reply_to, None, None, event)
    )


@on_message("dspam", allow_stan=True, Bad_user=True, enable_log=True)
@special
async def delaySpam(client: Client, message: Message):
    if len(message.command) < 4:
        return await Pbxbot.delete(message, "**Usage:** `.dspam <count> <delay> <message>`")
    try:
        count = int(message.command[1])
    except ValueError:
        return await Pbxbot.delete(message, "Give me a valid number.")
    try:
        delay = float(message.command[2])
    except ValueError:
        return await Pbxbot.delete(message, "Give me a valid delay (seconds).")

    reply_to = message.reply_to_message.id if message.reply_to_message else None
    to_spam  = message.text.split(" ", 3)[3].strip()
    event    = asyncio.Event()

    _register_task(message.chat.id, event)
    await message.delete()
    await asyncio.create_task(
        spam_text(client, message.chat.id, to_spam, count, reply_to, delay, None, event)
    )


@on_message("mspam", allow_stan=True, Bad_user=True, enable_log=True)
@special
async def mediaSpam(client: Client, message: Message):
    if not message.reply_to_message:
        return await Pbxbot.delete(message, "Reply to a media to spam.")
    if len(message.command) < 2:
        return await Pbxbot.delete(message, "Give me a valid number.")
    try:
        count = int(message.command[1])
    except ValueError:
        return await Pbxbot.delete(message, "Give me a valid number.")

    copy_id = message.reply_to_message.id
    event   = asyncio.Event()

    _register_task(message.chat.id, event)
    await message.delete()
    await asyncio.create_task(
        spam_text(client, message.chat.id, None, count, None, None, copy_id, event)
    )


@on_message("stopspam", allow_stan=True, Bad_user=True, enable_log=True)
async def stopSpam(_, message: Message):
    chat_id = message.chat.id
    if not spamTask.get(chat_id):
        return await Pbxbot.delete(message, "No spam task running in this chat.")

    for event in spamTask[chat_id]:
        event.set()

    chat_name = message.chat.title or message.chat.first_name
    del spamTask[chat_id]
    await Pbxbot.delete(message, f"**Spam stopped** in {chat_name}.")


@on_message("listspam", allow_stan=True, Bad_user=True, enable_log=True)
async def listSpam(_, message: Message):
    active = list(spamTask.keys())
    if not active:
        return await Pbxbot.edit(message, "**No active spam tasks.**")

    text = "**Active Spam Tasks:**\n\n"
    for cid in active:
        text += f"{Symbols.anchor} `{cid}`\n"
    await Pbxbot.edit(message, text)


# ══════════════════════════════════════════════════════════════════
#  HELP
# ══════════════════════════════════════════════════════════════════

HelpMenu("spam").add(
    "spam",
    "<count> <message>",
    "Spam a message x times.",
    ".spam 10 hi",
    "Spamming may get you banned.",
).add(
    "dspam",
    "<count> <delay> <message>",
    "Spam with delay (seconds).",
    ".dspam 10 1 hi",
    "Spamming may get you banned.",
).add(
    "mspam",
    "<count> <reply to media>",
    "Spam a media x times.",
    ".mspam 10",
    "Spamming may get you banned.",
).add(
    "stopspam",
    None,
    "Stop all spam in this chat.",
    ".stopspam",
    "Chat dependent.",
).add(
    "listspam",
    None,
    "List all active spam tasks.",
    ".listspam",
).info("Spam Messages").done()
