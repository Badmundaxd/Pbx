# G: Glass Buttons

from math import ceil

from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineQueryResultPhoto, InlineKeyboardMarkup

from Pbxbot.core import ENV, Symbols, db, Config
from Pbxbot.functions.templates import help_template

from Pbxbot.core.clients import Pbxbot
bot = Pbxbot.bot

# ── Color cycle: PRIMARY (blue) → SUCCESS (green) → DANGER (red) ──
_COLORS = [
    enums.ButtonStyle.PRIMARY,   # Blue
    enums.ButtonStyle.SUCCESS,   # Green
    enums.ButtonStyle.DANGER,    # Red
]

def _color(index: int) -> enums.ButtonStyle:
    """Har button ko alag color — index ke hisaab se cycle karo."""
    return _COLORS[index % len(_COLORS)]


def gen_inline_keyboard(collection: list, row: int = 2) -> list[list[InlineKeyboardButton]]:
    keyboard = []
    for i in range(0, len(collection), row):
        kyb = []
        for x in collection[i : i + row]:
            button = btn(*x)
            kyb.append(button)
        keyboard.append(kyb)
    return keyboard


def btn(text, value, type="callback_data") -> InlineKeyboardButton:
    return InlineKeyboardButton(text, **{type: value})


async def gen_inline_help_buttons(page: int, plugins: list) -> tuple[list, int]:
    buttons = []
    column = await db.get_env(ENV.btn_in_help) or 5
    column = int(column)
    emoji = await db.get_env(ENV.help_emoji) or "✧"
    pairs = list(map(list, zip(plugins[::2], plugins[1::2])))

    if len(plugins) % 2 == 1:
        pairs.append([plugins[-1]])

    max_pages = ceil(len(pairs) / column)
    pairs = [pairs[i : i + column] for i in range(0, len(pairs), column)]

    color_index = 0  # Global counter — har button alag color

    for pair in pairs[page]:
        btn_pair = []
        for i, plugin in enumerate(pair):
            if i % 2 == 0:
                btn_pair.append(
                    InlineKeyboardButton(
                        f"{emoji} {plugin}",
                        f"help_menu:{page}:{plugin}",
                        style=_color(color_index),
                    )
                )
            else:
                btn_pair.append(
                    InlineKeyboardButton(
                        f"{plugin} {emoji}",
                        f"help_menu:{page}:{plugin}",
                        style=_color(color_index),
                    )
                )
            color_index += 1
        buttons.append(btn_pair)

    # Navigation buttons — fixed colors
    buttons.append(
        [
            InlineKeyboardButton(
                Symbols.previous,
                f"help_page:{(max_pages - 1) if page == 0 else (page - 1)}",
                style=enums.ButtonStyle.PRIMARY,   # Blue ◀
            ),
            InlineKeyboardButton(
                Symbols.close,
                "help_data:c",
                style=enums.ButtonStyle.DANGER,    # Red ✕
            ),
            InlineKeyboardButton(
                Symbols.next,
                f"help_page:{0 if page == (max_pages - 1) else (page + 1)}",
                style=enums.ButtonStyle.SUCCESS,   # Green ▶
            ),
        ]
    )

    return buttons, max_pages


async def gen_bot_help_buttons() -> list[list[InlineKeyboardButton]]:
    buttons = []
    plugins = sorted(Config.BOT_CMD_MENU)
    emoji = await db.get_env(ENV.help_emoji) or "✧"
    pairs = list(map(list, zip(plugins[::2], plugins[1::2])))

    if len(plugins) % 2 == 1:
        pairs.append([plugins[-1]])

    color_index = 0  # Har button alag color

    for pair in pairs:
        btn_pair = []
        for i, plugin in enumerate(pair):
            if i % 2 == 0:
                btn_pair.append(
                    InlineKeyboardButton(
                        f"{emoji} {plugin}",
                        f"bot_help_menu:{plugin}",
                        style=_color(color_index),
                    )
                )
            else:
                btn_pair.append(
                    InlineKeyboardButton(
                        f"{plugin} {emoji}",
                        f"bot_help_menu:{plugin}",
                        style=_color(color_index),
                    )
                )
            color_index += 1
        buttons.append(btn_pair)

    # Bottom nav buttons
    buttons.append(
        [
            InlineKeyboardButton(
                "˹ ʜᴏᴍᴇ ˼",
                "help_data:start",
                style=enums.ButtonStyle.PRIMARY,   # Blue
            ),
            InlineKeyboardButton(
                Symbols.close,
                "help_data:botclose",
                style=enums.ButtonStyle.DANGER,    # Red
            ),
        ]
    )

    return buttons

def start_button() -> list[list[InlineKeyboardButton]]:
    color_index = 0
    return [
        [
            InlineKeyboardButton(" 📗 ᴀʙᴏᴜᴛ ", "help_data:bothelp", style=_color(color_index)),
            InlineKeyboardButton(" 💌 ᴏᴡɴᴇʀ ", url="https://t.me/BadMundaXD", style=_color(color_index + 1)),
            ],
        [
            InlineKeyboardButton(" 💡 ɢᴜɪᴅᴇ ", "help_data:source", style=_color(color_index + 2)),
        ],
        [
            InlineKeyboardButton("˹ ʜᴇʟᴘ ˼" ,  url="https://t.me/PBXCHATS", style=_color(color_index + 3)),
            InlineKeyboardButton("˹ υᴘᴅᴧᴛєs ˼" ,  url="https://t.me/PBX_UPDATE", style=_color(color_index + 4)),
    ]
    ]

@bot.on_inline_query(filters.regex("help_menu"))
async def inline_help(client: Client, inline_query):
    buttons, _ = await gen_inline_help_buttons(0, sorted(Config.CMD_MENU.keys()))
    help_text = await help_template(
        "Owner Name",
        (len(Config.CMD_MENU), len(Config.BOT_CMD_MENU)),
        (0, 1),
    )
    results = [
        InlineQueryResultPhoto(
            id="help_menu",
            photo_url="https://files.catbox.moe/upmgl2.png",
            thumb_url="https://files.catbox.moe/upmgl2.png",
            caption=help_text,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    ]
    await inline_query.answer(results, cache_time=0)
