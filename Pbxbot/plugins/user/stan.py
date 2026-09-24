from pyrogram import Client
from pyrogram.types import Message

from . import Config, HelpMenu, db, Pbxbot, on_message, special


# ===================== LIST STANS =====================

@on_message("stan", allow_stan=True)
async def stanUsers(client: Client, message: Message):
    msg = await Pbxbot.edit(message, "__Fetching stan users...__")

    users = await db.get_stans(client.me.id)
    if not users:
        return await Pbxbot.delete(msg, "__No stan users found!__")

    text = f"**Total stans:** `{len(users)}`\n\n"
    for u in users:
        uid = u["user_id"]
        try:
            user = await client.get_users(uid)
            mention = user.mention
        except Exception:
            mention = "Unknown User"
        text += f"• {mention} (`{uid}`)\n"

    await msg.edit(text)


# ===================== ADD STAN =====================

@on_message("addsudo", allow_stan=False, enable_log=True)
async def addStan(client: Client, message: Message):
    if message.from_user.id not in Config.AUTH_USERS:
        return await Pbxbot.delete(
            message, "__You are not authorized to use this command!__"
        )

    if message.reply_to_message:
        user = message.reply_to_message.from_user
    elif len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
        except Exception:
            return await Pbxbot.delete(message, "__Invalid user!__")
    else:
        return await Pbxbot.delete(
            message, "__Reply to a user or give a user ID!__"
        )

    if user.id == client.me.id:
        return await Pbxbot.delete(message, "__I can't add myself as a stan!__")

    if await db.is_stan(client.me.id, user.id):
        return await Pbxbot.delete(message, "__This user is already a stan!__")

    await db.add_stan(client.me.id, user.id)

    Config.AUTH_USERS.add(user.id)
    Config.STAN_USERS.add(user.id)

    await Pbxbot.delete(message, f"__Added {user.mention} as a stan!__")


# ===================== REMOVE STAN =====================

@on_message("rmsudo", allow_stan=False, enable_log=True)
@special
async def removeStan(client: Client, message: Message):
    if message.from_user.id not in Config.AUTH_USERS:
        return await Pbxbot.delete(
            message, "__You are not authorized to use this command!__"
        )

    if message.reply_to_message:
        user = message.reply_to_message.from_user
    elif len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
        except Exception:
            return await Pbxbot.delete(message, "__Invalid user!__")
    else:
        return await Pbxbot.delete(
            message, "__Reply to a user or give a user ID!__"
        )

    if not await db.is_stan(client.me.id, user.id):
        return await Pbxbot.delete(message, "__This user is not a stan!__")

    await db.rm_stan(client.me.id, user.id)

    Config.AUTH_USERS.discard(user.id)
    Config.STAN_USERS.discard(user.id)

    await Pbxbot.delete(message, f"__Removed {user.mention} from stans!__")


# ===================== HELP MENU =====================

HelpMenu("sudo").add(
    "stan",
    None,
    "Get a list of stan (sudo) users.",
    "stan",
    "Stan users can use limited sudo commands.",
).add(
    "addsudo",
    "<reply/username/userid>",
    "Add a user as a stan.",
    "addsudo",
    "Only authorized users can add stans.",
).add(
    "rmsudo",
    "<reply/username/userid>",
    "Remove a user from stans.",
    "rmsudo",
).info(
    "Stan (Sudo) Users"
).done()
