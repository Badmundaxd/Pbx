import asyncio
import re

from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.types import Message

from . import HelpMenu, custom_handler, db, handler, Pbxbot, on_message, Config


@on_message("filter", allow_stan=True, Bad_user=True)
async def set_filter(client: Client, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await Pbxbot.delete(
            message, f"Reply to a message with {handler}filter <keyword> to save it as a filter."
        )

    keyword = await Pbxbot.input(message)
    Pbx = await Pbxbot.edit(message, f"Saving filter `{keyword}`")
    msg = await message.reply_to_message.forward(Config.LOGGER_ID)

    await db.set_filter(client.me.id, message.chat.id, keyword.lower(), msg.id)
    await Pbxbot.delete(Pbx, f"**🍀 𝖭𝖾𝗐 𝖥𝗂𝗅𝗍𝖾𝗋 𝖲𝖺𝗏𝖾𝖽:** `{keyword}`")
    await msg.reply_text(
        f"**🍀 𝖭𝖾𝗐 𝖥𝗂𝗅𝗍𝖾𝗋 𝖲𝖺𝗏𝖾𝖽:** `{keyword}`\n\n**DO NOT DELETE THIS MESSAGE!!!**",
    )


@on_message(["rmfilter", "rmallfilter"], allow_stan=True, Bad_user=True)
async def rmfilter(client: Client, message: Message):
    if len(message.command[0]) < 9:
        if len(message.command) < 2:
            return await Pbxbot.delete(message, "Give a filter name to remove.")

        keyword = await Pbxbot.input(message)
        Pbx = await Pbxbot.edit(message, f"Removing filter `{keyword}`")

        if await db.is_filter(client.me.id, message.chat.id, keyword.lower()):
            await db.rm_filter(client.me.id, message.chat.id, keyword.lower())
            await Pbxbot.delete(Pbx, f"**🍀 𝖥𝗂𝗅𝗍𝖾𝗋 𝖱𝖾𝗆𝗈𝗏𝖾𝖽:** `{keyword}`")
        else:
            await Pbxbot.delete(Pbx, f"**🍀 𝖥𝗂𝗅𝗍𝖾𝗋 𝖽𝗈𝖾𝗌 𝗇𝗈𝗍 𝖾𝗑𝗂𝗌𝗍𝗌:** `{keyword}`")
    else:
        Pbx = await Pbxbot.edit(message, "Removing all filters...")

        await db.rm_all_filters(client.me.id, message.chat.id)
        await Pbxbot.delete(Pbx, "All filters have been removed.")


@on_message(["getfilter", "getfilters"], allow_stan=True, Bad_user=True)
async def allfilters(client: Client, message: Message):
    if len(message.command) > 1:
        keyword = await Pbxbot.input(message)
        Pbx = await Pbxbot.edit(message, f"Getting filter `{keyword}`")

        if await db.is_filter(client.me.id, message.chat.id, keyword.lower()):
            data = await db.get_filter(client.me.id, message.chat.id, keyword.lower())
            msgid = data["filter"][0]["msgid"]
            sent = await client.copy_message(message.chat.id, Config.LOGGER_ID, msgid)

            await sent.reply_text(f"**🍀 𝖥𝗂𝗅𝗍𝖾𝗋:** `{keyword}`")
            await Pbx.delete()

        else:
            await Pbxbot.delete(Pbx, f"**🍀 𝖥𝗂𝗅𝗍𝖾𝗋 𝖽𝗈𝖾𝗌 𝗇𝗈𝗍 𝖾𝗑𝗂𝗌𝗍𝗌:** `{keyword}`")

    else:
        Pbx = await Pbxbot.edit(message, "Getting all filters...")
        filters = await db.get_all_filters(client.me.id, message.chat.id)

        if filters:
            text = f"**🍀 𝖭𝗈. 𝗈𝖿 𝖥𝗂𝗅𝗍𝖾𝗋𝗌 𝗂𝗇 𝗍𝗁𝗂𝗌 𝖼𝗁𝖺𝗍:** `{len(filters)}`\n\n"

            for i, filter in enumerate(filters, 1):
                text += f"** {'0' if i < 10 else ''}{i}:** `{filter['keyword']}`\n"

            await Pbx.edit(text)

        else:
            await Pbxbot.delete(Pbx, "No filters in this chat.")


@custom_handler(filters.incoming & ~filters.service)
async def handle_filters(client: Client, message: Message):
    data = await db.get_all_filters(client.me.id, message.chat.id)
    if not data:
        return

    msg = message.text or message.caption
    if not msg:
        return

    for filter in data:
        pattern = r"( |^|[^\w])" + re.escape(filter["keyword"]) + r"( |$|[^\w])"
        if re.search(pattern, msg, flags=re.IGNORECASE):
            msgid = filter["msgid"]
            await client.copy_message(message.chat.id, Config.LOGGER_ID, msgid)
            await asyncio.sleep(1)


HelpMenu("filters").add(
    "filter",
    "<keyword> <reply to a message>",
    "Saves the replied message as a filter to given keyword along the command.",
    "filter Pbxbot 4.0",
    "You need to reply to the message you want to save as filter. You can also save media as filters alonng with captions.",
).add(
    "rmfilter",
    "<keyword>",
    "Removes the filter with given keyword.",
    "rmfilter Pbxbot 4.0",
).add(
    "rmallfilter",
    None,
    "Removes all the filters in current chat.",
    "rmallfilter",
).add(
    "getfilter",
    "<keyword>",
    "Gives the filter data associated with given keyword.",
    "getfilter Pbxbot 4.0",
).add(
    "getfilters", None, "Gets all filters in the chat.", "getfilters"
).info(
    "Filter Module"
).done()
