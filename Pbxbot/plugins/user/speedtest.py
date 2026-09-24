import io
import re
import subprocess
import sys
import traceback

import bs4
import requests
from pyrogram import Client
from pyrogram.errors import MessageTooLong
from pyrogram.types import Message
from speedtest import Speedtest
from . import HelpMenu, Pbxbot, on_message


@on_message("speedtest", allow_stan=True, Bad_user=True)
async def speed_test(_, message):
    Pbx = await Pbxbot.edit(message, "`testing speed...`")

    speed = Speedtest()
    speed.get_best_server()

    await Pbx.edit("`calculating download speed...`")
    speed.download()

    await Pbx.edit("`calculating upload speed...`")
    speed.upload()

    await Pbx.edit("`finising up...`")
    speed.results.share()
    result = speed.results.dict()

    form = """**𝖲𝗉𝖾𝖾𝖽𝖳𝖾𝗌𝗍 𝖱𝖾𝗌𝗎𝗅𝗍𝗌 🍀**

    **✧ 𝖨𝖲𝖯:** `{0}, {1}` 
    **✧ 𝖯𝗂𝗇𝗀:** `{2}`
    **✧ 𝖲𝖾𝗋𝗏𝖾𝗋:** `{3}, {4}`
    **✧ 𝖲𝗉𝗈𝗇𝗌𝗈𝗋:** `{5}`
    """

    await message.reply_photo(
        result["share"],
        caption=form.format(
            result["client"]["isp"],
            result["client"]["country"],
            result["ping"],
            result["server"]["name"],
            result["server"]["country"],
            result["server"]["sponsor"],
        )
    )
    await Pbx.delete()


HelpMenu("speedtest").add(
    "speedtest",
    None,
    "Test the speed of server and client.",
    "speedtest",
).info(
    "Speedtest"
).done()
