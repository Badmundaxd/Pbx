from pyrogram import idle

from Pbxbot import __version__
from Pbxbot.core import (
    Config,
    GachaBotsSetup,
    TemplateSetup,
    UserSetup,
    db,
    Pbxbot,
)

from Pbxbot.functions.tools import initialize_git
from Pbxbot.functions.utility import BList, Flood, TGraph

import asyncio
import warnings

# ─────────────────────────────────────────────
# Hide useless warnings
# ─────────────────────────────────────────────

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# Silence asyncio shutdown spam
# ─────────────────────────────────────────────

def silence_asyncio_exception(loop, context):
    pass

# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

async def main():

    await Pbxbot.startup()

    await db.connect()

    await UserSetup()
    await GachaBotsSetup()
    await TemplateSetup()

    await Flood.updateFromDB()
    await BList.updateBlacklists()

    await TGraph.setup()

    await initialize_git(Config.PLUGINS_REPO)

    await Pbxbot.start_message(__version__)

    await idle()

# ─────────────────────────────────────────────
# Start Bot
# ─────────────────────────────────────────────

if __name__ == "__main__":

    import sys

    if sys.version_info >= (3, 7):

        loop = asyncio.get_event_loop()

        # Hide asyncio spam
        loop.set_exception_handler(silence_asyncio_exception)

        try:

            loop.run_until_complete(main())

        finally:

            try:

                pending = asyncio.all_tasks(loop)

                for task in pending:
                    task.cancel()

                loop.run_until_complete(
                    asyncio.gather(*pending, return_exceptions=True)
                )

            except:
                pass

            loop.close()

    else:

        asyncio.run(main())
