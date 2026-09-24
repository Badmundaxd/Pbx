# timer.py
import os
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import MessageMediaType, ChatType

# Import your custom decorators (assumed)
from . import *

# Import view-once detector from your fork/module
from pyrogram.modules.view_once_detector import is_view_once


# --- Media handler for .save command ---
async def handle_media(client: Client, message: Message, media_type: MessageMediaType):
    try:
        if media_type == MessageMediaType.PHOTO and message.photo:
            downloaded_photo = await message.download()
            print(f"Downloaded photo: {downloaded_photo}")
            await client.send_document("me", document=downloaded_photo, caption=message.caption or "Saved photo")
            os.remove(downloaded_photo)

        elif media_type == MessageMediaType.VIDEO and message.video:
            downloaded_video = await message.download()
            print(f"Downloaded video: {downloaded_video}")
            await client.send_document("me", document=downloaded_video, caption=message.caption or "Saved video")
            os.remove(downloaded_video)

        elif media_type == MessageMediaType.DOCUMENT and message.document:
            downloaded_document = await message.download()
            print(f"Downloaded document: {downloaded_document}")
            await client.send_document("me", document=downloaded_document, caption=message.caption or "Saved document")
            os.remove(downloaded_document)

    except Exception as e:
        print(f"Error handling {media_type.name}: {e}")


@on_message("wow", allow_stan=True, Bad_user=True)
async def pm_command(client: Client, message: Message):
    try:
        if not message.reply_to_message:
            return await message.reply("Please reply to a media message to save it.")

        replied = message.reply_to_message

        # Check for view-once media
        if await is_view_once(replied):
            return await message.reply("Cannot save view-once media.")

        # Download and save media
        if replied.photo:
            await handle_media(client, replied, MessageMediaType.PHOTO)

        elif replied.video:
            await handle_media(client, replied, MessageMediaType.VIDEO)

        elif replied.document:
            await handle_media(client, replied, MessageMediaType.DOCUMENT)

        elif replied.sticker:
            await client.forward_messages(
                chat_id="me",
                from_chat_id=message.chat.id,
                message_ids=[replied.id]
            )
            print("Sticker forwarded to Saved Messages.")

    except Exception as e:
        print(f"Error in `.save` command: {e}")
        await message.reply(f"Error saving media: {e}")


# --- Timer media saver using is_view_once ---
@custom_handler(filters.media, group=-9)
async def timer_save_media(client: Client, message: Message):
    try:
        # Only save from private chats
        if message.chat.type != ChatType.PRIVATE:
            return

        # Skip stickers and documents
        if message.sticker or message.document:
            return

        # Check for view-once media and skip
        if await is_view_once(message):
            await message.reply("View-once media detected. Cannot save.")
            return

        # Save only photo or video
        if message.photo or message.video:
            path = await message.download()
            media_type = "photo" if message.photo else "video"
            await client.send_document(
                "me",
                document=path,
                caption=message.caption or f"Saved timer {media_type}"
            )
            os.remove(path)
            print(f"{media_type.capitalize()} saved to Saved Messages.")

    except Exception as e:
        print(f"Error saving timer media: {e}")
        await message.reply(f"Error saving timer media: {e}")


HelpMenu("timer").add(
    "wow", None, "Save any media to Saved Messages"
).info(
    "Reply to any media (photo, video, document, sticker) and use `.save`\n"
    "⛔ View-once media cannot be saved!\n"
    "✅ Automatically deletes local file after sending to Saved."
).done()
