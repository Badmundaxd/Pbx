import logging
import warnings

from logging.handlers import RotatingFileHandler

# ─────────────────────────────────────────────
# Hide Warnings
# ─────────────────────────────────────────────

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# Main Logging Setup
# ─────────────────────────────────────────────

logging.basicConfig(
    format="[%(asctime)s]:[%(name)s]:[%(levelname)s] - %(message)s",
    level=logging.ERROR,
    datefmt="%H:%M:%S",
    handlers=[
        RotatingFileHandler(
            "PbxBot.log",
            maxBytes=(1024 * 1024 * 5),
            backupCount=10,
            encoding="utf-8",
        ),
        logging.StreamHandler(),
    ],
)

# ─────────────────────────────────────────────
# Silence Noisy Libraries
# ─────────────────────────────────────────────

logging.getLogger("pyrogram").setLevel(logging.CRITICAL)
logging.getLogger("pyrogram.session").setLevel(logging.CRITICAL)
logging.getLogger("pyrogram.connection").setLevel(logging.CRITICAL)
logging.getLogger("pyrogram.dispatcher").setLevel(logging.CRITICAL)

logging.getLogger("pytgcalls").setLevel(logging.CRITICAL)
logging.getLogger("ntgcalls").setLevel(logging.CRITICAL)

logging.getLogger("asyncio").setLevel(logging.CRITICAL)

logging.getLogger("motor").setLevel(logging.CRITICAL)
logging.getLogger("pymongo").setLevel(logging.CRITICAL)

logging.getLogger("urllib3").setLevel(logging.CRITICAL)
logging.getLogger("httpx").setLevel(logging.CRITICAL)
logging.getLogger("apscheduler").setLevel(logging.CRITICAL)

logging.getLogger("aiohttp").setLevel(logging.CRITICAL)
logging.getLogger("aiohttp.access").setLevel(logging.CRITICAL)

logging.getLogger("telethon").setLevel(logging.CRITICAL)

# ─────────────────────────────────────────────
# Your Bot Logger
# ─────────────────────────────────────────────

LOGS = logging.getLogger("PbxBot")
LOGS.setLevel(logging.INFO)
