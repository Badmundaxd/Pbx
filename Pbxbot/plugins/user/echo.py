import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from Pbxbot.core import Symbols

from . import HelpMenu, custom_handler, db, Pbxbot, on_message


# ─────────────────────────────────────────────
#  HELPER — resolve user safely
# ─────────────────────────────────────────────
async def _resolve_user(client: Client, message: Message):
    """Get user id from reply or command argument. Returns (user_id, error)."""
    if message.reply_to_message:
        sender = message.reply_to_message.from_user
        if not sender:
            return None, "❌ Cannot resolve user (anonymous/bot)."
        return sender.id, None
    elif len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
            return user.id, None
        except Exception:
            return None, "❌ User not found! Please provide a valid username or ID."
    return None, None  # no argument given


# ─────────────────────────────────────────────
#  .echo — enable echo for a user
# ─────────────────────────────────────────────
@on_message("echo", allow_stan=True)
async def echo(client: Client, message: Message):
    user_id, err = await _resolve_user(client, message)

    if err:
        return await Pbxbot.delete(message, err)
    if not user_id:
        return await Pbxbot.delete(
            message, "Reply to a user or provide a user id/username!"
        )

    if await db.is_echo(client.me.id, message.chat.id, user_id):
        return await Pbxbot.delete(message, "⚠️ Echo is already enabled for this user!")

    await db.set_echo(client.me.id, message.chat.id, user_id)
    await Pbxbot.delete(message, f"✅ Echo ON — User `{user_id}`")


# ─────────────────────────────────────────────
#  .unecho — disable echo for a user
# ─────────────────────────────────────────────
@on_message("unecho", allow_stan=True)
async def unecho(client: Client, message: Message):
    user_id, err = await _resolve_user(client, message)

    if err:
        return await Pbxbot.delete(message, err)
    if not user_id:
        return await Pbxbot.delete(
            message, "Reply to a user or provide a user id/username!"
        )

    if not await db.is_echo(client.me.id, message.chat.id, user_id):
        return await Pbxbot.delete(message, "⚠️ Echo is already disabled for this user!")

    await db.rm_echo(client.me.id, message.chat.id, user_id)
    await Pbxbot.delete(message, f"🔕 Echo OFF — User `{user_id}`")


# ─────────────────────────────────────────────
#  .listecho — list all echoed users in this chat
# ─────────────────────────────────────────────
@on_message("listecho", allow_stan=True)
async def listecho(client: Client, message: Message):
    echos = await db.get_all_echo(client.me.id, message.chat.id)
    if not echos:
        return await Pbxbot.delete(message, "📭 No echoes active in this chat!")

    text = "**📋 Echo List (this chat):**\n\n"
    for user in echos:
        text += f"  {Symbols.anchor} `{user}`\n"

    await Pbxbot.send_message(message.chat.id, text)


# ─────────────────────────────────────────────
#  .clearecho — remove all echoes in this chat  [NEW]
# ─────────────────────────────────────────────
@on_message("clearecho", allow_stan=True)
async def clearecho(client: Client, message: Message):
    echos = await db.get_all_echo(client.me.id, message.chat.id)
    if not echos:
        return await Pbxbot.delete(message, "📭 No echoes active in this chat!")

    for user_id in echos:
        await db.rm_echo(client.me.id, message.chat.id, user_id)

    await Pbxbot.delete(message, f"🗑️ Cleared {len(echos)} echo(es) from this chat!")


# ─────────────────────────────────────────────
#  .echoall — enable echo for everyone in chat  [NEW]
#  (stores -1 as a special "all users" flag)
# ─────────────────────────────────────────────
@on_message("echoall", allow_stan=True)
async def echoall(client: Client, message: Message):
    ALL_FLAG = -1
    if await db.is_echo(client.me.id, message.chat.id, ALL_FLAG):
        return await Pbxbot.delete(message, "⚠️ EchoAll is already enabled in this chat!")

    await db.set_echo(client.me.id, message.chat.id, ALL_FLAG)
    await Pbxbot.delete(message, "✅ EchoAll ON — Every message in this chat will be echoed!")


@on_message("unechoall", allow_stan=True)
async def unechoall(client: Client, message: Message):
    ALL_FLAG = -1
    if not await db.is_echo(client.me.id, message.chat.id, ALL_FLAG):
        return await Pbxbot.delete(message, "⚠️ EchoAll is already disabled!")

    await db.rm_echo(client.me.id, message.chat.id, ALL_FLAG)
    await Pbxbot.delete(message, "🔕 EchoAll OFF")


# ─────────────────────────────────────────────
#  CORE HANDLER — echo incoming messages
# ─────────────────────────────────────────────
@custom_handler(filters.incoming & ~filters.service)
async def echo_handler(client: Client, message: Message):
    # Fix: anonymous sender crash
    if not message.from_user:
        return

    ALL_FLAG = -1
    is_specific = await db.is_echo(client.me.id, message.chat.id, message.from_user.id)
    is_all      = await db.is_echo(client.me.id, message.chat.id, ALL_FLAG)

    if not (is_specific or is_all):
        return

    await asyncio.sleep(1)

    try:
        if message.sticker:
            await message.reply_sticker(message.sticker.file_id)
        elif message.text:
            await message.reply(message.text)
        elif message.photo:
            await message.reply_photo(message.photo.file_id, caption=message.caption or "")
        elif message.video:
            await message.reply_video(message.video.file_id, caption=message.caption or "")
        elif message.audio:
            await message.reply_audio(message.audio.file_id, caption=message.caption or "")
        elif message.voice:
            await message.reply_voice(message.voice.file_id)
        elif message.video_note:
            await message.reply_video_note(message.video_note.file_id)
        elif message.animation:
            await message.reply_animation(message.animation.file_id, caption=message.caption or "")
        elif message.document:
            await message.reply_document(message.document.file_id, caption=message.caption or "")
    except Exception:
        pass  # silently ignore flood / permission errors


# ─────────────────────────────────────────────
#  .resend / .copy — resend a replied message
# ─────────────────────────────────────────────
@on_message(["resend", "copy"], allow_stan=True)
async def reSend(_, message: Message):
    if message.reply_to_message:
        await message.reply_to_message.copy(message.chat.id)
    await message.delete()


# ─────────────────────────────────────────────
#  HELP MENU
# ─────────────────────────────────────────────
HelpMenu("echo").add(
    "echo",
    "<reply> or <userid>",
    "Echo every message of the replied user in the present chat!",
    "echo @username",
    "Supports text, sticker, photo, video, audio, voice, animation & documents!",
).add(
    "unecho",
    "<reply> or <userid>",
    "Stop echoing messages of the replied user in the present chat!",
    "unecho @username",
).add(
    "listecho",
    None,
    "List all users whose messages are being echoed in this chat!",
    "listecho",
).add(
    "clearecho",
    None,
    "Remove all active echoes in this chat at once!",
    "clearecho",
).add(
    "echoall",
    None,
    "Echo every message from every user in this chat!",
    "echoall",
).add(
    "unechoall",
    None,
    "Disable EchoAll in this chat!",
    "unechoall",
).add(
    "resend",
    "<reply>",
    "Resend the replied message! (alias: .copy)",
    "resend",
).info(
    "Is it Echoing? 🔊"
).done()
