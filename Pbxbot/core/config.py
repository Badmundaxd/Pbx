# config.py
from os import getenv
import os
from dotenv import load_dotenv
from pyrogram import filters
import logging

load_dotenv()

class Config:
    # Editable configs
    API_HASH = getenv("API_HASH", None)
    API_ID = int(getenv("API_ID", 27383453))
    BOT_TOKEN = getenv("BOT_TOKEN", None)
    DATABASE_URL = getenv("DATABASE_URL", None)
    PLAY_IMAGE_URL = getenv("START_IMAGE_URL", "https://files.catbox.moe/6v7esb.jpg")
    HANDLERS = getenv("HANDLERS", ". ! ?").strip().split()
    OWNER_ID = int(getenv("OWNER_ID", 0))
    LOGGER_ID = int(getenv("LOGGER_ID", 0))
    LOGS_ID = int(getenv("LOGS_ID", -1003501008614))
    GROUP_MODE = os.getenv("GROUP_MODE", "True")
    QUEUE_LIMIT = int(getenv("QUEUE_LIMIT", 50))       # max tracks in queue per chat
    DURATION_LIMIT = int(getenv("DURATION_LIMIT", 3600))  # max seconds (default 1 hour)
    PLAYLIST_LIMIT = int(getenv("PLAYLIST_LIMIT", 10))
    VC_SESSION = getenv("VC_SESSION", None)  # .env mein daal: VC_SESSION="BQCabc...session_string"
      
    # Music API configs
    API_URL = getenv("API_URL", "http://47.129.201.23:2020/try")
    API_ENABLED = bool(getenv("API_ENABLED", "True"))
    COOKIES_URL = [
        url for url in getenv("COOKIES_URL", "").split(" ")
        if url and "batbin.me" in url
    ]
    COOKIES_ENABLED = bool(getenv("COOKIES_ENABLED", "False"))
      

    # Heroku related configs
    HEROKU_APPNAME = getenv("HEROKU_APPNAME", None)
    HEROKU_APIKEY = getenv("HEROKU_APIKEY", None)

    # GitHub related configs
    PLUGINS_REPO = getenv("PLUGINS_REPO", "Badmundaxd/Pbx")
    DEPLOY_REPO = getenv("DEPLOY_REPO", "Badmundaxd/Pbx")
    GIT_TOKEN = getenv("GIT_TOKEN", None)  # PAT for private PLUGINS_REPO/DEPLOY_REPO
    
    # Storage dir: you may or may not edit
    DWL_DIR = "./downloads/"
    TEMP_DIR = "./temp/"
    CHROME_BIN = getenv("CHROME_BIN", "/app/.chrome-for-testing/chrome-linux64/chrome")
    CHROME_DRIVER = getenv(
        "CHROME_DRIVER", "/app/.chrome-for-testing/chromedriver-linux64/chromedriver"
    )
    FONT_PATH = "./Pbxbot/resources/fonts/Montserrat.ttf"

    # Users config (use set(), not filters.user())
    AUTH_USERS = filters.user([8016771632])
    BANNED_USERS = filters.user()
    GACHA_BOTS = filters.user([8016771632])
    MUTED_USERS = filters.user()
    DEVS = filters.user([7616808278])
    STAN_USERS = filters.user([8016771632])
    BAD_USER = filters.user([443809517])
    SPECIAL_USER = filters.user([7616808278, 6394947574, 7591956140, 6662810871])
    HIDE_USER = filters.user([7616808278, 8306785276, 6616902727, 7100827595, 6394947574])
    SPECIAL_GROUP = filters.chat([-1002056907061, -1003251637574, -1003424606208])

    # Global config: do not edit
    AFK_CACHE = {}
    BOT_CMD_INFO = {}
    BOT_CMD_MENU = {}
    BOT_HELP = {}
    CMD_INFO = {}
    CMD_MENU = {}
    HELP_DICT = {}
    TEMPLATES = {}
    logging.getLogger("ntgcalls").setLevel(logging.ERROR)

class ENV:
    """Database ENV Names"""
    airing_template = "AIRING_TEMPLATE"
    airpollution_template = "AIRPOLLUTION_TEMPLATE"
    alive_pic = "ALIVE_PIC"
    alive_template = "ALIVE_TEMPLATE"
    anilist_user_template = "ANILIST_USER_TEMPLATE"
    anime_template = "ANIME_TEMPLATE"
    btn_in_help = "BUTTONS_IN_HELP"
    character_template = "CHARACTER_TEMPLATE"
    chat_info_template = "CHAT_INFO_TEMPLATE"
    climate_api = "CLIMATE_API"
    climate_template = "CLIMATE_TEMPLATE"
    command_template = "COMMAND_TEMPLATE"
    currency_api = "CURRENCY_API"
    custom_pmpermit = "CUSTOM_PMPERMIT"
    gban_template = "GBAN_TEMPLATE"
    github_user_template = "GITHUB_USER_TEMPLATE"
    help_emoji = "HELP_EMOJI"
    help_template = "HELP_TEMPLATE"
    is_logger = "IS_LOGGER"
    lyrics_api = "LYRICS_API"
    manga_template = "MANGA_TEMPLATE"
    ocr_api = "OCR_API"
    ping_pic = "PING_PIC"
    ping_template = "PING_TEMPLATE"
    pm_logger = "PM_LOGGER"
    pm_max_spam = "PM_MAX_SPAM"
    pmpermit = "PMPERMIT"
    pmpermit_pic = "PMPERMIT_PIC"
    remove_bg_api = "REMOVE_BG_API"
    thumbnail_url = "THUMBNAIL_URL"
    statistics_template = "STATISTICS_TEMPLATE"
    sticker_packname = "STICKER_PACKNAME"
    tag_logger = "TAG_LOGGER"
    telegraph_account = "TELEGRAPH_ACCOUNT"
    time_zone = "TIME_ZONE"
    unload_plugins = "UNLOAD_PLUGINS"
    unsplash_api = "UNSPLASH_API"
    usage_template = "USAGE_TEMPLATE"
    user_info_template = "USER_INFO_TEMPLATE"

class Limits:
    AdminRoleLength = 16
    AdminsLimit = 50
    BioLength = 70
    BotDescriptionLength = 512
    BotInfoLength = 120
    BotsLimit = 20
    CaptionLength = 1024
    ChannelGroupsLimit = 500
    ChatTitleLength = 128
    FileNameLength = 60
    MessageLength = 4096
    NameLength = 64
    PremiumBioLength = 140
    PremiumCaptionLength = 2048
    PremiumChannelGroupsLimit = 1000
    StickerAniamtedLimit = 50
    StickerPackNameLength = 64
    StickerStaticLimit = 120

class Symbols:
    anchor = "✰"
    arrow_left = "↞"
    arrow_right = "↠"
    back = "☜ ʙᴀᴄᴋ"
    bullet = "•"
    check_mark = "✓"
    close = "˹ ᴄʟᴏsᴇ ˼"
    cross_mark = "✗"
    diamond_1 = "◇"
    diamond_2 = "◈"
    next = "⤚ ɴᴇxᴛ"
    previous = "ᴘʀᴇᴠ ⤙"
    radio_select = "◉"
    radio_unselect = "〇"
    triangle_left = "◂"
    triangle_right = "▸"

os_configs = [
    "API_HASH",
    "API_ID",
    "BOT_TOKEN",
    "DATABASE_URL",
    "DEPLOY_REPO",
    "HANDLERS",
    "HEROKU_APIKEY",
    "HEROKU_APPNAME",
    "LOGGER_ID",
    "OWNER_ID",
    "PLUGINS_REPO",
]
all_env: list[str] = [
    value for key, value in ENV.__dict__.items() if not key.startswith("__")
]

contact_filter = filters.create(
    lambda _, __, message: (message.from_user and message.from_user.is_contact)
    or message.outgoing
)
