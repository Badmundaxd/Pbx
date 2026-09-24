import datetime

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from Pbxbot.core import ENV, LOGS

from . import custom_handler, db, Pbxbot, on_message

import time as _time

# ── Env cache — DB hit sirf ek baar, phir 2 min tak memory se ──
_env_cache: dict = {}
_CACHE_TTL = 120

async def _cached_get_env(key: str):
    entry = _env_cache.get(key)
    if entry and _time.time() - entry[1] < _CACHE_TTL:
        return entry[0]
    result = await db.get_env(key)
    _env_cache[key] = (result, _time.time())
    return result


@on_message("save", allow_stan=True, Bad_user=True)
async def save_message(client: Client, message: Message):
    if len(message.command) >= 2:
        to_save = message.command[1]
        await client.send_message(
            "me",
            f"Saved on {datetime.datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}:\n\n```{to_save}```",
            disable_web_page_preview=True,
        )
    elif message.reply_to_message:
        to_save = message.reply_to_message.id
        await client.forward_messages(
            "me",
            message.chat.id,
            to_save,
        )
    await message.delete()


@custom_handler(filters.incoming & filters.group & filters.mentioned & ~filters.service)
async def tag_logger(client: Client, message: Message):
    tag_gc = await _cached_get_env(ENV.tag_logger)  # ✅ cached
    if not tag_gc:
        return

    if message.from_user.is_bot:
        return

    if not message.mentioned:
        return

    msg = await message.forward(int(tag_gc), True)
    await Pbxbot.bot.send_message(
        int(tag_gc),
        f"{message.from_user.mention} **tagged** {client.me.mention} **in** {message.chat.title} (`{message.chat.id}`)",
        disable_web_page_preview=True,
        reply_to_message_id=msg.id,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Go to Tag 📨", url=message.link)]]),
    )


@custom_handler(filters.incoming & filters.private & ~filters.bot & ~filters.service)
async def pm_logger(client: Client, message: Message):
    if message.from_user.id == 777000:
        return

    logger = await _cached_get_env(ENV.pm_logger)  # ✅ cached
    try:
        if logger:
            if message.chat.id != client.me.id:
                await message.forward(int(logger), True)
    except Exception as e:
        LOGS.warning(f"PM Logger Err: {e}")
