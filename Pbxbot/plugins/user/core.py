import importlib
import os
import sys
from pathlib import Path

from pyrogram import Client, filters
from pyrogram.enums import MessagesFilter, ParseMode
from pyrogram.types import InlineQueryResultPhoto
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent

from Pbxbot.core import ENV, Config, Symbols

from . import HelpMenu, bot, db, handler, Pbxbot, on_message

@on_message("help", allow_stan=True, Bad_user=True)
async def help(client: Client, message: Message):
    Pbx = await Pbxbot.edit(message, "**Processing...**")
    if len(message.command) == 1:
        try:
            result = await client.get_inline_bot_results(bot.me.username, "help_menu")
            await client.send_inline_bot_result(
                message.chat.id,
                result.query_id,
                result.results[0].id,
                True,
            )
            return await Pbx.delete()
        except Exception as e:
            await Pbxbot.error(Pbx, str(e), 20)
            return

    plugin = await Pbxbot.input(message)
    if plugin.lower() in Config.CMD_MENU:
        try:
            await Pbxbot.edit(
                Pbx, Config.CMD_MENU[plugin.lower()], ParseMode.MARKDOWN
            )
            return
        except Exception as e:
            await Pbxbot.error(Pbx, str(e), 20)
            return

    available_plugins = f"{Symbols.bullet} **𝖠𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾 𝗉𝗅𝗎𝗀𝗂𝗇𝗌:**\n\n"
    for i in sorted(list(Config.CMD_MENU.keys())):
        available_plugins += f"`{i}`, "
    available_plugins = available_plugins[:-2]
    available_plugins += (
        f"\n\n𝖣𝗈 `{handler}help <plugin name>` 𝗍𝗈 𝗀𝖾𝗍 𝖽𝖾𝗍𝖺𝗂𝗅𝖾𝖽 𝗂𝗇𝖿𝗈 𝗈𝖿 𝗍𝗁𝖺𝗍 𝗉𝗅𝗎𝗀𝗂𝗇."
    )
    await Pbxbot.edit(Pbx, available_plugins, ParseMode.MARKDOWN)

@on_message("plinfo", allow_stan=True, Bad_user=True)
async def plugin_info(_, message: Message):
    plugin = await Pbxbot.input(message)
    if plugin.lower() in Config.CMD_MENU:
        try:
            await Pbxbot.edit(
                message, Config.CMD_MENU[plugin.lower()], ParseMode.MARKDOWN
            )
            return
        except Exception as e:
            await Pbxbot.error(message, str(e), 20)
            return
    await Pbxbot.error(message, f"**Invalid Plugin Name:** `{plugin}`", 20)


@on_message("cmdinfo", allow_stan=True, Bad_user=True)
async def command_info(_, message: Message):
    cmd = await Pbxbot.input(message)
    if cmd.lower() in Config.CMD_INFO:
        try:
            cmd_dict = Config.CMD_INFO[cmd.lower()]
            template = (
                f"**🍀 𝖯𝗅𝗎𝗀𝗂𝗇:** `{cmd_dict['plugin']}.py`\n\n"
                f"**{Symbols.anchor} 𝖢𝗈𝗆𝗆𝖺𝗇𝖽:** `{cmd_dict['command']}`\n"
                f"**{Symbols.anchor} 𝖣𝖾𝗌𝖼𝗋𝗂𝗉𝗍𝗂𝗈𝗇:** __{cmd_dict['description']}__\n"
                f"**{Symbols.anchor} 𝖤𝗑𝖺𝗆𝗉𝗅𝖾:** `{cmd_dict['example']}`\n"
                f"**{Symbols.anchor} 𝖭𝗈𝗍𝖾:** __{cmd_dict['note']}__\n"
            )
            await Pbxbot.edit(message, template, ParseMode.MARKDOWN)
            return
        except Exception as e:
            await Pbxbot.error(message, str(e), 20)
            return
    await Pbxbot.error(message, f"**Invalid Command Name:** `{cmd}`", 20)




HelpMenu("help").add(
    "help",
    "<plugin name>",
    "Get the detailed help menu for that mentioned plugin or get the whole help menu instead.",
    "help alive",
).add("repo", None, "Get the repo link of the bot.", "repo").add(
    "plinfo",
    "<plugin name>",
    "Get the detailed info of the mentioned plugin.",
    "plinfo alive",
).add(
    "cmdinfo",
    "<command name>",
    "Get the detailed info of the mentioned command.",
    "cmdinfo alive",
    )
