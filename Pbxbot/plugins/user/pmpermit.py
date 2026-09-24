import random
import time
from pyrogram.enums import ChatType
from pyrogram import Client, filters, enums
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultPhoto,
    CallbackQuery,
)

from Pbxbot.core import ENV
from . import Config, HelpMenu, Symbols, custom_handler, db, Pbxbot, on_message, bot

# ══════════════════════════════════════════════════════════════════
#  IN-MEMORY CACHE — MongoDB hits zero karne ke liye
#  Har incoming PM pe 4+ DB queries hundi si — ab memory se chalega
# ══════════════════════════════════════════════════════════════════
_CACHE_TTL = 120  # 2 minute

_pmoff_cache: dict = {}       # {client_id: (bool, ts)}
_pmpermit_cache: dict = {}    # {(client_id, user_id): (bool, ts)}
_env_cache: dict = {}         # {key: (value, ts)}


async def _cached_is_pmoff(client_id: int) -> bool:
    entry = _pmoff_cache.get(client_id)
    if entry and time.time() - entry[1] < _CACHE_TTL:
        return entry[0]
    result = await db.is_pmoff(client_id)
    _pmoff_cache[client_id] = (result, time.time())
    return result


async def _cached_is_pmpermit(client_id: int, user_id: int) -> bool:
    key = (client_id, user_id)
    entry = _pmpermit_cache.get(key)
    if entry and time.time() - entry[1] < _CACHE_TTL:
        return entry[0]
    result = await db.is_pmpermit(client_id, user_id)
    _pmpermit_cache[key] = (result, time.time())
    return result


def _invalidate_pmpermit(client_id: int, user_id: int):
    _pmpermit_cache.pop((client_id, user_id), None)


def _invalidate_pmoff(client_id: int):
    _pmoff_cache.pop(client_id, None)


async def _cached_get_env(key: str):
    entry = _env_cache.get(key)
    if entry and time.time() - entry[1] < _CACHE_TTL:
        return entry[0]
    result = await db.get_env(key)
    _env_cache[key] = (result, time.time())
    return result

# ══════════════════════════════════════════════════════════════════

blocked_messages = [
    "🤐 User has entered the silent zone.",
    "👻 Message blocked. Ghost mode activated.",
    "🏖️ Sorry, the user is on vacation in Blockland.",
    "🚫 Message blocked. Time for a digital forcefield.",
    "🚷 User temporarily ejected from my DM.",
    "🌑 Blocking vibes only. Silence in progress.",
    "🔇 Shhh... message blocked for tranquility.",
    "🚷 Access denied. User in the digital timeout corner.",
    "⛔ User temporarily MIA from the conversation.",
    "🔒 Message blocked. Secret mission engaged.",
]
unblocked_messages = [
    "🎉 Welcome back! Digital barrier lifted.",
    "🌊 Unblocked! Get ready for a flood of messages.",
    "🗝️ User released from message jail. Freedom at last!",
    "🔓 Breaking the silence!.",
    "📬 User back on the radar. Messages unlocked!",
    "🚀 Soaring back into the conversation!",
    "🌐 Reconnecting user to the chat matrix.",
    "📈 Unblocking for an influx of communication!",
    "🚀 Launching user back into the message cosmos!",
    "🎙️ Unblocked and ready for the conversation spotlight!",
]
WARNS = {}
PREV_MESSAGE = {}


# ── Auth check — same as callbacks.py ────────────────────────
async def check_auth_click(cb: CallbackQuery) -> bool:
    if cb.from_user.id not in Config.AUTH_USERS:
        await cb.answer(
            "You are not authorized to use this bot. \n\n</> @ll_THE_BAD_BOT_ll",
            show_alert=True,
        )
        return False
    return True


@on_message("block", allow_stan=True, Bad_user=True)
async def block_user(client: Client, message: Message):
    if len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
        except Exception as e:
            return await Pbxbot.error(message, f"`{e}`")
    elif message.chat.type == ChatType.PRIVATE:
        user = message.chat
    elif message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        return await Pbxbot.delete(
            message, "`Reply to a user or give their id/username`"
        )

    if user.id == client.me.id:
        return await Pbxbot.delete(message, "`I can't block myself`")

    if user.id in Config.DEVS:
        return await Pbxbot.delete(message, "`I can't block my devs`")

    success = await client.block_user(user.id)
    if success:
        await Pbxbot.delete(
            message,
            f"**{random.choice(blocked_messages)}\n\n{Symbols.cross_mark} Blocked:** {user.mention}",
        )
    else:
        await Pbxbot.error(message, f"`Couldn't block {user.mention}`")


@on_message("unblock", allow_stan=True, Bad_user=True)
async def unblock_user(client: Client, message: Message):
    if len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
        except Exception as e:
            return await Pbxbot.error(message, f"`{e}`")
    elif message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        return await Pbxbot.delete(
            message, "`Reply to a user or give their id/username`"
        )

    if user.id == client.me.id:
        return await Pbxbot.delete(message, "`I can't unblock myself`")

    success = await client.unblock_user(user.id)
    if success:
        await Pbxbot.delete(
            message,
            f"**{random.choice(unblocked_messages)}\n\n{Symbols.check_mark} Unblocked:** {user.mention}",
        )
    else:
        await Pbxbot.error(message, f"`Couldn't unblock {user.mention}`")


@on_message(["allow", "approve"], allow_stan=True, Bad_user=True)
async def allow_pm(client: Client, message: Message):
    if len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
            user_id = user.id
            user_mention = user.mention
        except Exception as e:
            return await Pbxbot.error(message, f"`{e}`")
    elif message.chat.type == ChatType.PRIVATE:
        user_id = message.chat.id
        user_mention = message.chat.first_name or message.chat.title
    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_mention = message.reply_to_message.from_user.mention
    else:
        return await Pbxbot.delete(
            message, "`Reply to a user or give their id/username`"
        )

    if user_id == client.me.id:
        return await Pbxbot.delete(message, "`I can't allow myself`")

    if await _cached_is_pmpermit(client.me.id, user_id):
        return await Pbxbot.delete(message, "`User is already allowed to pm!`")

    await db.add_pmpermit(client.me.id, user_id)
    _invalidate_pmpermit(client.me.id, user_id)  # cache refresh
    await Pbxbot.delete(message, f"**{Symbols.check_mark} Allowed:** {user_mention}")


@on_message(["disallow", "disapprove"], allow_stan=True, Bad_user=True)
async def disallow_pm(client: Client, message: Message):
    if len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
            user_id = user.id
            user_mention = user.mention
        except Exception as e:
            return await Pbxbot.error(message, f"`{e}`")
    elif message.chat.type == ChatType.PRIVATE:
        user_id = message.chat.id
        user_mention = message.chat.first_name or message.chat.title
    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_mention = message.reply_to_message.from_user.mention
    else:
        return await Pbxbot.delete(
            message, "`Reply to a user or give their id/username`"
        )

    if user_id == client.me.id:
        return await Pbxbot.delete(message, "`I can't disallow myself`")

    if not await _cached_is_pmpermit(client.me.id, user_id):
        return await Pbxbot.delete(message, "`User is not allowed to pm!`")

    await db.rm_pmpermit(client.me.id, user_id)
    _invalidate_pmpermit(client.me.id, user_id)  # cache refresh
    await Pbxbot.delete(
        message, f"**{Symbols.cross_mark} Disallowed:** {user_mention}"
    )


@on_message(["allowlist", "approvelist"], allow_stan=True, Bad_user=True)
async def allowlist(client: Client, message: Message):
    Pbx = await Pbxbot.edit(message, "`Fetching allowlist...`")
    users = await db.get_all_pmpermits(client.me.id)
    if not users:
        return await Pbx.edit("`No users allowed to pm!`")

    text = "**🍀 𝖠𝗉𝗉𝗋𝗈𝗏𝖾𝖽 𝖴𝗌𝖾𝗋'𝗌 𝖫𝗂𝗌𝗍:**\n\n"
    for user in users:
        try:
            name = (await client.get_users(user["user"])).first_name
            text += f"    {Symbols.anchor} {name} (`{user['user']}`) | {user['date']}\n"
        except:
            text += f"    {Symbols.anchor} Unknown Peer (`{user['user']}`) | {user['date']}\n"

    await Pbx.edit(text)


@on_message("pmoff", allow_stan=True, Bad_user=True)
async def pm_off(client: Client, message: Message):
    if await _cached_is_pmoff(client.me.id):
        return await Pbxbot.delete(message, "`PM permit is already disabled!`")
    await db.set_pmoff(client.me.id, True)
    _invalidate_pmoff(client.me.id)  # cache refresh
    await Pbxbot.delete(message, "**✅ PM Permit has been disabled for this session.**")


@on_message("pmon", allow_stan=True, Bad_user=True)
async def pm_on(client: Client, message: Message):
    if not await _cached_is_pmoff(client.me.id):
        return await Pbxbot.delete(message, "`PM permit is already enabled!`")
    await db.set_pmoff(client.me.id, False)
    _invalidate_pmoff(client.me.id)  # cache refresh
    await Pbxbot.delete(message, "**✅ PM Permit has been enabled for this session.**")


@custom_handler(filters.incoming & filters.private & ~filters.bot & ~filters.service)
async def handle_incoming_pm(client: Client, message: Message):
    if message.from_user.id in Config.DEVS or message.from_user.id == 777000:
        return

    # ✅ Cached — no MongoDB hit on every PM
    if await _cached_is_pmoff(client.me.id):
        return

    if await _cached_is_pmpermit(client.me.id, message.from_user.id):
        return

    if message.from_user.id in Config.AUTH_USERS:
        return

    # ✅ Cached env — fetched once, reused for 2 min
    max_spam = await _cached_get_env(ENV.pm_max_spam)
    max_spam = int(max_spam) if max_spam else 3
    warns = WARNS.get(client.me.id, {}).get(message.from_user.id, max_spam)

    if warns <= 0:
        await client.block_user(message.from_user.id)
        WARNS[client.me.id] = {message.from_user.id: max_spam}
        return await client.send_message(
            message.chat.id,
            "**🚨 Enough of your spamming! Blocking you.**"
        )

    bot_info = await client.get_me()
    owner_name = bot_info.first_name
    owner_mention = f"[{owner_name}](tg://user?id={bot_info.id})"

    pm_msg = "👻 **𝐏ʙ𝐗ʙᴏᴛ 4.0  𝐏ᴍ 𝐒ᴇᴄ𝘂𝗿𝗶𝘁𝘆** 👻\n\n"
    custom_pmmsg = await _cached_get_env(ENV.custom_pmpermit)  # ✅ cached

    if custom_pmmsg:
        pm_msg += f"{custom_pmmsg}\n\n☠ 𝐘𝗈𝗎 𝐇𝖺𝗏𝖾 {warns} 𝐖𝖺𝗋𝗇𝗂𝗇𝗀𝗌 𝐋𝖾𝖿𝗍! ☠"
    else:
        pm_msg += (
            f"👋🏻 **𝐇ყ 𝐈 𝐀m {message.from_user.mention}!**\n"
            "❤️ **𝐎ɯɳҽɾ 𝐈ʂ 𝐎ϝϝℓιɳҽ 𝐒ꪮ 𝐏ℓꫀαʂꫀ 𝐃σɳ'ƚ 𝐒ραɱ🌪️**\n"
            "⚡ **𝐈ϝ 𝐘συ 𝐒ραɱ , 𝐘συ 𝐖ιℓℓ 𝐁ҽ 𝐁ℓσ¢ƙҽԃ 𝐀υƚσɱαƚι¢ℓℓү 🌸**\n"
            f"🦋 **𝐖αιт 𝐅σя  𝐌у 𝐂υтє {owner_mention} ❤️**\n\n"
            f"☠ **𝐘𝗈𝗎 𝗁𝖺𝗏𝖾 {warns} 𝐖𝖺𝗋𝗇𝗂𝗇𝗀𝗌 𝐋𝖾𝖿𝗍!** ☠"
        )

    try:
        result = await client.get_inline_bot_results(
            bot.me.username,
            f"pmpermit_menu_{message.from_user.id}_{client.me.id}"
        )
        await client.send_inline_bot_result(
            message.chat.id,
            result.query_id,
            result.results[0].id,
            True,
        )
    except Exception as e:
        print(f"Error in PM Permit Inline: {e}")

    WARNS.setdefault(client.me.id, {})[message.from_user.id] = warns - 1


@bot.on_inline_query(filters.regex(r"pmpermit_menu_(\d+)_(\d+)"))
async def inline_pmpermit(client: Client, inline_query):
    user_id = int(inline_query.matches[0].group(1))
    owner_id = int(inline_query.matches[0].group(2))

    try:
        bot_info = await client.get_users(owner_id)
        owner_name = bot_info.first_name
        owner_mention = f"[{owner_name}](tg://user?id={bot_info.id})"
    except:
        owner_mention = "Owner"

    pm_msg = "👻 **𝐏ʙ𝐗ʙᴏᴛ 4.0  𝐏ᴍ 𝐒ᴇᴄ𝘂𝗿𝗶𝘁𝘆** 👻\n\n"
    custom_pmmsg = await db.get_env(ENV.custom_pmpermit)
    warns = WARNS.get(owner_id, {}).get(user_id, 3)

    if custom_pmmsg:
        pm_msg += f"{custom_pmmsg}\n\n☠ 𝐘𝗈𝗎 𝗁𝖺𝗏𝖾 {warns} 𝗐𝖺𝗋𝗇𝗂𝗇𝗀𝗌 𝗅𝖾𝖿𝗍! ☠"
    else:
        pm_msg += (
            f"👋🏻 **𝐇ყ 𝐈 𝐀m {inline_query.from_user.mention}!**\n"
            "❤️ **𝐎ɯɳҽɾ 𝐈ʂ 𝐎ϝϝℓιɳҽ 𝐒ꪮ 𝐏ℓꫀαʂꫀ 𝐃σɳ'ƚ 𝐒ραɱ🌪️**\n"
            "⚡ **𝐈ϝ 𝐘συ 𝐒ραɱ , 𝐘συ 𝐖ιℓℓ 𝐁ҽ 𝐁ℓσ¢ƙҽԃ 𝐀υƚσɱαƚι¢ℓℓү 🌸**\n"
            f"🦋 **𝐖αιт 𝐅σя  𝐌у 𝐂υтє {owner_mention} ❤️**\n\n"
            f"☠ **𝐘𝗈𝗎 𝗁𝖺𝗏𝖾 {warns} 𝗐𝖺𝗋𝗇𝗂𝗇𝗀𝗌 𝗅𝖾𝖿𝗍!** ☠"
        )

    buttons = [
        [
            InlineKeyboardButton(
                "✅ Approve",
                callback_data=f"pm_approve_{user_id}_{owner_id}",
                style=enums.ButtonStyle.SUCCESS,    # 🟢 Green
            ),
            InlineKeyboardButton(
                "❌ Block",
                callback_data=f"pm_block_{user_id}_{owner_id}",
                style=enums.ButtonStyle.DANGER,     # 🔴 Red
            ),
        ],
        [
            InlineKeyboardButton(
                "🚫 Disallow",
                callback_data=f"pm_disallow_{user_id}_{owner_id}",
                style=enums.ButtonStyle.DANGER,     # 🔴 Red
            ),
            InlineKeyboardButton(
                "🔓 Unblock",
                callback_data=f"pm_unblock_{user_id}_{owner_id}",
                style=enums.ButtonStyle.PRIMARY,    # 🔵 Blue
            ),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)

    results = [
        InlineQueryResultPhoto(
            id=f"pmpermit_{user_id}_{owner_id}",
            photo_url="https://files.catbox.moe/em2tpa.png",
            thumb_url="https://files.catbox.moe/em2tpa.png",
            caption=pm_msg,
            reply_markup=reply_markup,
        )
    ]

    await inline_query.answer(results, cache_time=0)


@bot.on_callback_query(filters.regex(r"^pm_(approve|block|disallow|unblock)_(\d+)_(\d+)$"))
async def handle_pm_callback(client: Client, cb: CallbackQuery):

    # ── Step 1: Auth check ──────────────────────────────────────
    if not await check_auth_click(cb):
        return

    parts   = cb.data.split("_")
    # callback format: pm_<action>_<user_id>_<owner_id>
    action   = parts[1]
    user_id  = int(parts[2])
    owner_id = int(parts[3])

    # ── Step 2: Sahi userbot dhundo owner_id se ─────────────────
    # Pbxbot.users list mein se woh client jiska me.id == owner_id
    userbot = None
    for u in Pbxbot.users:
        if u.me and u.me.id == owner_id:
            userbot = u
            break

    if not userbot:
        await cb.answer("❌ Userbot session not found!", show_alert=True)
        return

    # ── Step 3: Action execute karo userbot se ──────────────────
    try:
        if action == "approve":
            if await _cached_is_pmpermit(owner_id, user_id):
                await cb.answer("ℹ️ User is already approved!", show_alert=True)
                return
            await db.add_pmpermit(owner_id, user_id)
            _invalidate_pmpermit(owner_id, user_id)  # cache refresh
            result_text = "✅ Approved — User can now PM freely."

        elif action == "block":
            await userbot.block_user(user_id)
            result_text = "❌ Blocked — User has been blocked."

        elif action == "disallow":
            if not await _cached_is_pmpermit(owner_id, user_id):
                await cb.answer("ℹ️ User was not in allowlist!", show_alert=True)
                return
            await db.rm_pmpermit(owner_id, user_id)
            _invalidate_pmpermit(owner_id, user_id)  # cache refresh
            result_text = "🚫 Disallowed — User removed from allowlist."

        elif action == "unblock":
            await userbot.unblock_user(user_id)
            result_text = "🔓 Unblocked — User has been unblocked."

        else:
            await cb.answer("❌ Unknown action!", show_alert=True)
            return

        # ── Step 4: Toast alert + message edit ──────────────────
        await cb.answer(result_text, show_alert=True)

        # Button ko update karo — done state dikhao
        await cb.edit_message_reply_markup(
            InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        f"☑️ {result_text}",
                        callback_data="pm_done",
                        style=enums.ButtonStyle.SUCCESS,
                    )
                ]
            ])
        )

    except Exception as e:
        await cb.answer(f"❌ Error: {str(e)}", show_alert=True)


# ── pm_done — sirf ek dummy handler taaki button crash na kare
@bot.on_callback_query(filters.regex(r"^pm_done$"))
async def pm_done_cb(_, cb: CallbackQuery):
    await cb.answer("✅ Action already completed!", show_alert=False)


# Help Menu
HelpMenu("pmpermit").add(
    "block",
    "<reply to user>/<userid/username>",
    "Block a user from pm-ing you.",
    "block @PBXCHATS",
).add(
    "unblock",
    "<reply to user>/<userid/username>",
    "Unblock a user from pm-ing you.",
    "unblock @PBXCHATS",
).add(
    "allow",
    "<reply to user>/<userid/username>",
    "Allow a user to pm you.",
    "allow @PBXCHATS",
    "An alias of 'approve' is also available.",
).add(
    "disallow",
    "<reply to user>/<userid/username>",
    "Disallow a user to pm you.",
    "disallow @PBXCHATS",
    "An alias of 'disapprove' is also available.",
).add(
    "allowlist",
    None,
    "List all users allowed to pm you.",
    "allowlist",
    "An alias of 'approvelist' is also available.",
).add(
    "pmon",
    None,
    "Enable PM permit security for this session.",
    "pmon",
).add(
    "pmoff",
    None,
    "Disable PM permit security for this session.",
    "pmoff",
).info(
    "Manage who can pm you and control PM permit status."
).done()
