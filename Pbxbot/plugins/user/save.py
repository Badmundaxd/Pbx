import os
import re
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.enums import MessageMediaType
from pyrogram.errors import UsernameNotOccupied, ChannelInvalid, ChannelPrivate

# Your custom decorators
from . import *

# View-once detector from your fork
from pyrogram.modules.view_once_detector import is_view_once

# ---------------------------
# MEDIA HANDLER FUNCTION
# ---------------------------
async def handle_media(client: Client, message: Message, media_type: MessageMediaType):
    try:
        file = await message.download()
        await client.send_document(
            "me",
            file,
            caption=message.caption or f"Saved {media_type.name.lower()}"
        )
        os.remove(file)
    except Exception as e:
        print(f"Error handling media: {e}")

# -----------------------------------------------------
# IMPROVED PARSE TELEGRAM LINK (Supports both public t.me/username/id and private t.me/c/id/id)
# -----------------------------------------------------
def parse_telegram_link(link: str):
    link = link.split("?")[0].strip("/")

    # Private channel/group link: t.me/c/123456789/1609
    private_match = re.match(r"t\.me/c/(\d+)(?:/(\d+))?", link)
    if private_match:
        chat_part = private_match.group(1)
        msg_id = int(private_match.group(2)) if private_match.group(2) else None
        chat_id = int("-100" + chat_part)
        return chat_id, msg_id

    # Public link: t.me/username/1609 or t.me/username
    public_match = re.match(r"t\.me/([^/\s]+)(?:/(\d+))?", link)
    if public_match:
        username = public_match.group(1)
        msg_id = int(public_match.group(2)) if public_match.group(2) else None
        return username, msg_id

    return None, None

# -----------------------------------------------------
# COMMAND: .save
# -----------------------------------------------------
@on_message("save", allow_stan=True, Bad_user=True)
async def save_command(client: Client, message: Message):
    try:
        # LINK METHOD
        if len(message.command) > 1:
            chat_identifier, msg_id = parse_telegram_link(message.command[1])

            if not chat_identifier or not msg_id:
                return await message.reply("❌ Invalid Telegram link or missing message ID")

            try:
                msg = await client.get_messages(chat_identifier, msg_id)
            except (UsernameNotOccupied, ChannelInvalid, ChannelPrivate):
                return await message.reply("❌ Cannot access the chat (invalid username, private or not joined)")

            if await is_view_once(msg):
                return await message.reply("⛔ View-once media cannot be saved")

            if msg.photo:
                await handle_media(client, msg, MessageMediaType.PHOTO)
            elif msg.video:
                await handle_media(client, msg, MessageMediaType.VIDEO)
            elif msg.document:
                await handle_media(client, msg, MessageMediaType.DOCUMENT)
            elif msg.voice:
                await handle_media(client, msg, MessageMediaType.VOICE)
            elif msg.audio:
                await handle_media(client, msg, MessageMediaType.AUDIO)
            elif msg.sticker:
                await client.forward_messages("me", chat_identifier, msg.id)
            else:
                return await message.reply("❌ No media found")

            return await message.reply("✔ Saved successfully")

        # REPLY METHOD
        if not message.reply_to_message:
            return await message.reply("Reply to a media or use `.save <link>`")

        replied = message.reply_to_message

        if await is_view_once(replied):
            return await message.reply("⛔ View-once media cannot be saved")

        if replied.photo:
            await handle_media(client, replied, MessageMediaType.PHOTO)
        elif replied.video:
            await handle_media(client, replied, MessageMediaType.VIDEO)
        elif replied.document:
            await handle_media(client, replied, MessageMediaType.DOCUMENT)
        elif replied.voice:
            await handle_media(client, replied, MessageMediaType.VOICE)
        elif replied.audio:
            await handle_media(client, replied, MessageMediaType.AUDIO)
        elif replied.sticker:
            await client.forward_messages("me", message.chat.id, replied.id)
        else:
            return await message.reply("❌ No media found")

        await message.reply("✔ Saved successfully")

    except Exception as e:
        await message.reply(f"❌ Error:\n`{e}`")

# -----------------------------------------------------
# COMMAND: .saveall
# -----------------------------------------------------
@on_message("saveall", allow_stan=True, Bad_user=True)
async def saveall_command(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("Usage:\n`.saveall <channel_link>` (link to a message or channel)")

    chat_identifier, start_id = parse_telegram_link(message.command[1])

    if not chat_identifier:
        return await message.reply("❌ Invalid Telegram link")

    # If no specific message ID, set to latest
    if start_id is None:
        start_id = 0  # Will start from latest

    try:
        status = await message.reply("🔄 Saving media...")

        saved = skipped = errors = 0

        async for msg in client.get_chat_history(chat_identifier, offset_id=start_id):
            try:
                if await is_view_once(msg):
                    skipped += 1
                    continue

                if msg.photo:
                    await handle_media(client, msg, MessageMediaType.PHOTO)
                elif msg.video:
                    await handle_media(client, msg, MessageMediaType.VIDEO)
                elif msg.document:
                    await handle_media(client, msg, MessageMediaType.DOCUMENT)
                elif msg.voice:
                    await handle_media(client, msg, MessageMediaType.VOICE)
                elif msg.audio:
                    await handle_media(client, msg, MessageMediaType.AUDIO)
                elif msg.sticker:
                    await client.forward_messages("me", chat_identifier, msg.id)
                else:
                    continue

                saved += 1

                if saved % 10 == 0:
                    await status.edit(
                        f"🔄 Saving...\n\n"
                        f"✅ Saved: {saved}\n"
                        f"⏭ Skipped: {skipped}\n"
                        f"❌ Errors: {errors}"
                    )

            except Exception:
                errors += 1

        await status.edit(
            f"✅ **SaveAll Done**\n\n"
            f"📁 Saved: {saved}\n"
            f"⏭ Skipped: {skipped}\n"
            f"❌ Errors: {errors}"
        )

    except (UsernameNotOccupied, ChannelInvalid, ChannelPrivate):
        await message.reply("❌ Cannot access the chat (invalid, private or not joined)")
    except Exception as e:
        await message.reply(f"❌ Error:\n`{e}`")

# ---------------------------
# HELP MENU
# ---------------------------
HelpMenu("private").add(
    "save", "<link or reply>", "Save media by reply or link (supports public & private channels)"
).add(
    "saveall", "<channel_link>", "Save all media from a channel starting from the given message (or latest)"
).info(
    "✔ Manual save only\n"
    "✔ No auto / timer saving\n"
    "✔ View-once blocked\n"
    "✔ Supports public (t.me/username/id) & private (t.me/c/id/id) links"
).done()
