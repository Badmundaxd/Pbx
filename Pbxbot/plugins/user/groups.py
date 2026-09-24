import asyncio
import random
import string
import time

from pyrogram import Client
from pyrogram.enums import ChatMembersFilter, ChatMemberStatus
from pyrogram.types import Message

from Pbxbot.functions.media import get_media_fileid
from Pbxbot.functions.templates import chat_info_templates

from . import HelpMenu, group_n_channel, Pbxbot, on_message


# ─────────────────────────────────────────────
#  HELPER — generate random pbxuserbot name
#  Letters shuffled randomly + timestamp suffix
#  e.g. pbxuserbot_xkqmbztaen_1712345678
# ─────────────────────────────────────────────
def _random_gc_name() -> str:
    letters = list(string.ascii_lowercase)   # a-z
    random.shuffle(letters)                  # shuffle every time → always different order
    suffix = "".join(letters[:10])           # pick 10 shuffled letters
    ts = str(int(time.time()))[-6:]          # last 6 digits of timestamp
    return f"pbxuserbot_{suffix}_{ts}"


kickme_quotes = [
    "✌️ Outta here, leaving the stage to the real stars!",
    "🚀 Elevating my vibes, leaving the chat in style.",
    "🕊️ Flying solo, exiting this group gracefully.",
    "🌪️ Stirring up the winds of departure, bye!",
    "🚶‍♂️ Walking away like a boss, see you never!",
    "🔥 Burning bridges and creating my own path. Adios!",
    "💫 Turning the page and closing this chapter.",
    "👑 Crown's too heavy for this chat. I'm out!",
    "🏃‍♂️ Sprinting out of here with flair. Catch you never!",
    "🚤 Sailing away from this group chat, smooth seas ahead!",
    "🍃 Like a leaf in the wind, I'm drifting away. Farewell!",
    "🛫 Taking off from this chat runway. Bon voyage!",
    "💼 Closing the briefcase on this chat. Professional exit!",
    "🎭 Exiting the stage with a dramatic flair. Ta-da!",
    "🎶 Playing my exit music. Cue the farewell symphony!",
    "🕶️ Fading into the shadows, leaving an air of mystery.",
    "🚪 Closing the door quietly on this chat. Exit complete!",
    "🔒 Locking the chat behind me. Keep it stylish, folks!",
    "🌌 Vanishing into the cosmic abyss. See you in the stars!",
    "💔 Breaking free from this chat. Unleashing my solo journey!",
]


# ─────────────────────────────────────────────
#  EXISTING COMMANDS (cleaned up)
# ─────────────────────────────────────────────

@on_message("setgpic", chat_type=group_n_channel, admin_only=True, allow_stan=True)
async def setgpic(_, message: Message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        return await Pbxbot.delete(message, "Reply to a photo to set it as the group profile picture.")

    status = await message.chat.set_photo(photo=message.reply_to_message.photo.file_id)
    if not status:
        return await Pbxbot.delete(message, "Sorry, something went wrong.")

    await Pbxbot.delete(message, "✅ Group profile picture updated!")
    await Pbxbot.check_and_log(
        "setgpic",
        f"**Group Profile Picture**\n\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`",
    )


@on_message("setgtitle", chat_type=group_n_channel, admin_only=True, allow_stan=True)
async def setgtitle(_, message: Message):
    if len(message.command) < 2:
        return await Pbxbot.delete(message, "Provide a title to set for this group.")

    prev_title = message.chat.title
    new_title = await Pbxbot.input(message)
    status = await message.chat.set_title(new_title)
    if not status:
        return await Pbxbot.delete(message, "Sorry, something went wrong.")

    await Pbxbot.delete(message, f"✅ Group title updated to `{new_title}`!")
    await Pbxbot.check_and_log(
        "setgtitle",
        f"**Group Title Changed**\n\n**Old:** `{prev_title}`\n**New:** `{new_title}`\n**Group ID:** `{message.chat.id}`",
    )


@on_message("setgabout", chat_type=group_n_channel, admin_only=True, allow_stan=True)
async def setgabout(_, message: Message):
    if len(message.command) < 2:
        return await Pbxbot.delete(message, "Provide a description to set for this group.")

    new_about = await Pbxbot.input(message)
    status = await message.chat.set_description(new_about)
    if not status:
        return await Pbxbot.delete(message, "Sorry, something went wrong.")

    await Pbxbot.delete(message, "✅ Group description updated!")
    await Pbxbot.check_and_log(
        "setgabout",
        f"**Group About Updated**\n\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`",
    )


@on_message("setgusername", chat_type=group_n_channel, admin_only=True, allow_stan=True)
async def setgusername(client: Client, message: Message):
    user_status = (await message.chat.get_member(message.from_user.id)).status
    if user_status != ChatMemberStatus.OWNER:
        return await Pbxbot.delete(message, "Only the group owner can change the username.")

    if len(message.command) < 2:
        return await Pbxbot.delete(message, "Provide a username to set for this group.")

    new_username = await Pbxbot.input(message)
    status = await client.set_chat_username(message.chat.id, new_username)
    if not status:
        return await Pbxbot.delete(message, "Sorry, something went wrong.")

    await Pbxbot.delete(message, f"✅ Group username set to `@{new_username}`!")
    await Pbxbot.check_and_log(
        "setgusername",
        f"**Group Username Changed**\n\n**Group:** `{message.chat.title}`\n**New Username:** `@{new_username}`",
    )


@on_message("getglink", chat_type=group_n_channel, admin_only=True, allow_stan=True)
async def getglink(_, message: Message):
    link = await message.chat.export_invite_link()
    await Pbxbot.delete(message, f"**Group Invite Link:** `{link}`")


@on_message("kickme", chat_type=group_n_channel, allow_stan=True, Bad_user=True)
async def kickme(client: Client, message: Message):
    Pbx = await Pbxbot.edit(message, random.choice(kickme_quotes))
    try:
        await client.leave_chat(message.chat.id)
    except Exception as e:
        return await Pbxbot.delete(Pbx, f"Can't leave this chat.\n**Error:** `{e}`")


@on_message("newgroup", allow_stan=True, Bad_user=True)
async def new_group(client: Client, message: Message):
    if len(message.command) < 2:
        return await Pbxbot.delete(message, "Provide a title for the new group.")

    new_title = await Pbxbot.input(message)
    try:
        grp = await client.create_group(new_title, Pbxbot.bot.me.id)
        await Pbxbot.edit(message, f"**Group Link:** [{grp.title}]({grp.invite_link})")
    except Exception as e:
        await Pbxbot.error(message, f"`{e}`", 20)


@on_message("newchannel", allow_stan=True, Bad_user=True)
async def new_channel(client: Client, message: Message):
    if len(message.command) < 2:
        return await Pbxbot.delete(message, "Provide a title for the new channel.")

    new_title = await Pbxbot.input(message)
    try:
        ch = await client.create_channel(new_title, "Created by Pbxbot")
        await Pbxbot.edit(message, f"**Channel Link:** [{ch.title}]({ch.username})")
    except Exception as e:
        await Pbxbot.error(message, f"`{e}`", 20)


# ─────────────────────────────────────────────
#  NEW: .creategc — create multiple GCs
#  Usage:
#    .creategc 5 public   → 5 public groups
#    .creategc 3 private  → 3 private groups
#    .creategc 10         → 10 private groups (default)
# ─────────────────────────────────────────────
@on_message("creategc", allow_stan=True, Bad_user=True)
async def creategc(client: Client, message: Message):
    args = message.command[1:]

    if not args:
        return await Pbxbot.delete(
            message,
            "Usage: `.creategc <count> [public/private]`\nExample: `.creategc 5 public`"
        )

    try:
        count = int(args[0])
    except ValueError:
        return await Pbxbot.delete(message, "❌ Count must be a number! Example: `.creategc 5 public`")

    if count < 1 or count > 50:
        return await Pbxbot.delete(message, "❌ Count must be between 1 and 50.")

    gc_type = args[1].lower() if len(args) > 1 else "private"
    if gc_type not in ("public", "private"):
        return await Pbxbot.delete(message, "❌ Type must be `public` or `private`.")

    Pbx = await Pbxbot.edit(message, f"⏳ Creating {count} {gc_type} group(s)...")

    results = []
    failed = 0

    for i in range(count):
        gc_name = _random_gc_name()
        try:
            grp = await client.create_group(gc_name, Pbxbot.bot.me.id)

            if gc_type == "public":
                # set a unique public username
                username = gc_name.replace("_", "")[:32]
                try:
                    await client.set_chat_username(grp.id, username)
                    link = f"t.me/{username}"
                except Exception:
                    link = await grp.export_invite_link()
            else:
                link = await grp.export_invite_link()

            results.append(f"`{i+1}.` [{gc_name}]({link})")
        except Exception as e:
            failed += 1
            results.append(f"`{i+1}.` ❌ Failed: `{e}`")

        await asyncio.sleep(1.5)  # avoid flood limits

    text = f"**✅ Created {count - failed}/{count} {gc_type} group(s):**\n\n"
    text += "\n".join(results)
    if failed:
        text += f"\n\n⚠️ {failed} group(s) failed."

    await Pbx.edit(text, disable_web_page_preview=True)


# ─────────────────────────────────────────────
#  NEW: .createchannel — create multiple channels
#  Usage:
#    .createchannel 5 public   → 5 public channels
#    .createchannel 3 private  → 3 private channels
#    .createchannel 10         → 10 private channels (default)
# ─────────────────────────────────────────────
@on_message("createchannel", allow_stan=True, Bad_user=True)
async def createchannel(client: Client, message: Message):
    args = message.command[1:]

    if not args:
        return await Pbxbot.delete(
            message,
            "Usage: `.createchannel <count> [public/private]`\nExample: `.createchannel 5 public`"
        )

    try:
        count = int(args[0])
    except ValueError:
        return await Pbxbot.delete(message, "❌ Count must be a number! Example: `.createchannel 5 public`")

    if count < 1 or count > 50:
        return await Pbxbot.delete(message, "❌ Count must be between 1 and 50.")

    ch_type = args[1].lower() if len(args) > 1 else "private"
    if ch_type not in ("public", "private"):
        return await Pbxbot.delete(message, "❌ Type must be `public` or `private`.")

    Pbx = await Pbxbot.edit(message, f"⏳ Creating {count} {ch_type} channel(s)...")

    results = []
    failed = 0

    for i in range(count):
        ch_name = _random_gc_name()
        try:
            ch = await client.create_channel(ch_name, "Created by Pbxbot Userbot")

            if ch_type == "public":
                username = ch_name.replace("_", "")[:32]
                try:
                    await client.set_chat_username(ch.id, username)
                    link = f"t.me/{username}"
                except Exception:
                    link = await ch.export_invite_link()
            else:
                link = await ch.export_invite_link()

            results.append(f"`{i+1}.` [{ch_name}]({link})")
        except Exception as e:
            failed += 1
            results.append(f"`{i+1}.` ❌ Failed: `{e}`")

        await asyncio.sleep(1.5)

    text = f"**✅ Created {count - failed}/{count} {ch_type} channel(s):**\n\n"
    text += "\n".join(results)
    if failed:
        text += f"\n\n⚠️ {failed} channel(s) failed."

    await Pbx.edit(text, disable_web_page_preview=True)


# ─────────────────────────────────────────────
#  EXISTING COMMANDS (unchanged logic, cleaned text)
# ─────────────────────────────────────────────

@on_message("chatinfo", allow_stan=True, Bad_user=True)
async def chatInfo(client: Client, message: Message):
    if len(message.command) > 1:
        try:
            chat = await client.get_chat(message.command[1])
        except Exception as e:
            return await Pbxbot.error(message, f"`{e}`")
    else:
        chat = message.chat

    Pbx = await Pbxbot.edit(message, "Fetching chat info...")

    if chat.invite_link:
        chat_link = f"[Invite Link]({chat.invite_link})"
    elif chat.username:
        chat_link = f"@{chat.username}"
    else:
        chat_link = "Private Chat"

    chat_owner = None
    admins_count = 0
    bots_count = 0

    async for admin in client.get_chat_members(chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
        admins_count += 1
        if admin.status == ChatMemberStatus.OWNER:
            chat_owner = admin.user.mention

    async for _ in client.get_chat_members(chat.id, filter=ChatMembersFilter.BOTS):
        bots_count += 1

    chat_info = await chat_info_templates(
        chatName=chat.title,
        chatId=chat.id,
        chatLink=chat_link,
        chatOwner=chat_owner,
        dcId=chat.dc_id,
        membersCount=chat.members_count,
        adminsCount=admins_count,
        botsCount=bots_count,
        description=chat.description,
    )

    if chat.photo:
        async for photo in client.get_chat_photos(chat.id, 1):
            await Pbx.delete()
            await client.send_photo(
                message.chat.id,
                photo.file_id,
                caption=chat_info,
                reply_to_message_id=message.id,
                disable_notification=True,
            )
            return
    else:
        await Pbx.edit(chat_info, disable_web_page_preview=True)


@on_message("chatadmins", allow_stan=True, Bad_user=True)
async def chatAdmins(client: Client, message: Message):
    if len(message.command) < 2:
        chat = message.chat
    else:
        try:
            chat = await client.get_chat(message.command[1])
        except Exception as e:
            return await Pbxbot.error(message, f"`{e}`")

    Pbx = await Pbxbot.edit(message, "Fetching chat admins...")

    admin_count = 0
    admins = "**💫 Admins in this chat:**\n\n"
    async for admin in client.get_chat_members(chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
        admin_count += 1
        admins += f"**{'0' if admin_count < 10 else ''}{admin_count}:** {admin.user.mention} — `{admin.status}`\n"

    await Pbx.edit(admins, disable_web_page_preview=True)


@on_message("chatbots", allow_stan=True, Bad_user=True)
async def chatBots(client: Client, message: Message):
    if len(message.command) < 2:
        chat = message.chat
    else:
        try:
            chat = await client.get_chat(message.command[1])
        except Exception as e:
            return await Pbxbot.error(message, f"`{e}`")

    Pbx = await Pbxbot.edit(message, "Fetching chat bots...")

    bot_count = 0
    bots = "**🤖 Bots in this chat:**\n\n"
    async for bot in client.get_chat_members(chat.id, filter=ChatMembersFilter.BOTS):
        bot_count += 1
        bots += f"**{'0' if bot_count < 10 else ''}{bot_count}:** @{bot.user.username}\n"

    await Pbx.edit(bots, disable_web_page_preview=True)


@on_message("id", allow_stan=True, Bad_user=True)
async def chatId(_, message: Message):
    msg = message.reply_to_message or message
    Pbx = await Pbxbot.edit(message, "Fetching message info...")

    info = f"**💫 Chat ID:** `{msg.chat.id}`\n"
    info += f"**🪪 Message ID:** `{msg.id}`\n\n"

    if msg.from_user:
        info += f"**👤 User ID:** `{msg.from_user.id}`\n\n"
    if msg.forward_from:
        info += f"**👤 Forwarded From:** `{msg.forward_from.id}`\n\n"
    if msg.forward_from_chat:
        info += f"**💫 Forwarded Chat ID:** `{msg.forward_from_chat.id}`\n\n"

    file_id = await get_media_fileid(msg)
    if file_id:
        info += f"**📁 File ID:** `{file_id}`\n\n"

    await Pbx.edit(info, disable_web_page_preview=True)


@on_message("invite", allow_stan=True, Bad_user=True)
async def inviteUser(client: Client, message: Message):
    if len(message.command) < 2:
        return await Pbxbot.delete(message, "Provide a username/id to invite to this chat.")

    users = (await Pbxbot.input(message)).split(" ")
    Pbx = await Pbxbot.edit(message, "Inviting users...")

    resolved_users = await client.get_users(users)
    await message.chat.add_members([user.id for user in resolved_users])
    await Pbx.edit("✅ Successfully invited users to this chat.")


# ─────────────────────────────────────────────
#  HELP MENU
# ─────────────────────────────────────────────
HelpMenu("groups").add(
    "setgpic", "<reply to photo>", "Set the group profile picture.", "setgpic"
).add(
    "setgtitle", "<title>", "Set the group title.", "setgtitle My Group"
).add(
    "setgabout", "<text>", "Set the group description.", "setgabout Some description"
).add(
    "setgusername", "<username>", "Set the group username (owner only).", "setgusername mygroup",
    "Give username without '@'."
).add(
    "getglink", None, "Get the group invite link.", "getglink"
).add(
    "kickme", None, "Leave the chat in swag 😎!", "kickme"
).add(
    "newgroup", "<title>", "Create a new group.", "newgroup My Group"
).add(
    "newchannel", "<title>", "Create a new channel.", "newchannel My Channel"
).add(
    "creategc",
    "<count> [public/private]",
    "Create multiple groups at once with random pbxuserbot names!",
    "creategc 5 public",
    "Count: 1–50 | Type: public or private (default: private) | Names are always random.",
).add(
    "createchannel",
    "<count> [public/private]",
    "Create multiple channels at once with random pbxuserbot names!",
    "createchannel 5 public",
    "Count: 1–50 | Type: public or private (default: private) | Names are always random.",
).add(
    "chatinfo", "<chat id (optional)>", "Get info about the chat.", "chatinfo"
).add(
    "chatadmins", "<chat id (optional)>", "Get the list of admins.", "chatadmins"
).add(
    "chatbots", "<chat id (optional)>", "Get the list of bots.", "chatbots"
).add(
    "id", "<reply (optional)>", "Get chat/user/message/file IDs.", "id"
).add(
    "invite", "<username/id>", "Invite a user to this chat.", "invite @username",
    "Separate multiple users with spaces."
).info(
    "Group & Channel Menu"
).done()
