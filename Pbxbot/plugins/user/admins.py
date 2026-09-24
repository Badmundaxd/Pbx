import asyncio
import time
from datetime import datetime, timedelta

from pyrogram import Client
from pyrogram.types import ChatPermissions, ChatPrivileges, Message

from Pbxbot.core import LOGS
from . import HelpMenu, group_only, handler, Pbxbot, on_message, Bad, special


@on_message(
    "promote",
    chat_type=group_only,
    admin_only=True,
    allow_stan=True,
    Bad_user=True,
    enable_log=True,
)
async def promote(client: Client, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await Pbxbot.delete(
            message, "Need a username/id or reply to a user to promote them!"
        )

    if message.reply_to_message:
        user = message.reply_to_message.from_user
        title = await Pbxbot.input(message)
    else:
        user = await client.get_users(message.command[1])
        title = (await Pbxbot.input(message)).split(" ", 1)[1].strip() if len(message.command) > 2 else ""

    try:
        privileges = ChatPrivileges(
            can_manage_chat=True,
            can_delete_messages=True,
            can_manage_video_chats=True,
            can_restrict_members=False,
            can_promote_members=False,
            can_change_info=False,
            can_invite_users=True,
            can_pin_messages=True,
            is_anonymous=False,
        )
        await message.chat.promote_member(user.id, privileges)
        if title:
            await client.set_administrator_title(message.chat.id, user.id, title)
    except Exception as e:
        return await Pbxbot.error(message, f"Error promoting user: {e}")

    await Pbxbot.delete(message, f"**💫 Promoted {user.mention} successfully!**")
    await Pbxbot.check_and_log(
        "promote",
        f"**Promoted User**\n\n**User:** {user.mention}\n**User ID:** `{user.id}`\n**Title:** `{title or 'None'}`\n**Admin:** {message.from_user.mention}\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`",
    )


@on_message(
    "fullpromote",
    chat_type=group_only,
    admin_only=True,
    allow_stan=True,
    Bad_user=True,
    enable_log=True,
)
async def fullpromote(client: Client, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await Pbxbot.delete(
            message, "Need a username/id or reply to a user to full-promote them!"
        )

    if message.reply_to_message:
        user = message.reply_to_message.from_user
        title = await Pbxbot.input(message)
    else:
        user = await client.get_users(message.command[1])
        title = (await Pbxbot.input(message)).split(" ", 1)[1].strip() if len(message.command) > 2 else ""

    try:
        privileges = ChatPrivileges(
            can_manage_chat=True,
            can_delete_messages=True,
            can_manage_video_chats=True,
            can_restrict_members=True,
            can_promote_members=True,
            can_change_info=True,
            can_invite_users=True,
            can_pin_messages=True,
            is_anonymous=False,
        )
        await message.chat.promote_member(user.id, privileges)
        if title:
            await client.set_administrator_title(message.chat.id, user.id, title)
    except Exception as e:
        return await Pbxbot.error(message, f"Error full-promoting user: {e}")

    await Pbxbot.delete(message, f"**🌟 Full-Promoted {user.mention} successfully!**")
    await Pbxbot.check_and_log(
        "fullpromote",
        f"**Full-Promoted User**\n\n**User:** {user.mention}\n**User ID:** `{user.id}`\n**Title:** `{title or 'None'}`\n**Admin:** {message.from_user.mention}\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`",
    )


@on_message(
    "demote",
    chat_type=group_only,
    admin_only=True,
    allow_stan=True,
    Bad_user=True,
    enable_log=True,
)
@Bad
async def demote(client: Client, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await Pbxbot.delete(
            message, "Need a username/id or reply to a user to demote them!"
        )

    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        user = await client.get_users(message.command[1])

    try:
        privileges = ChatPrivileges(
            can_manage_chat=False,
            can_delete_messages=False,
            can_manage_video_chats=False,
            can_restrict_members=False,
            can_promote_members=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False,
            is_anonymous=False,
        )
        await message.chat.promote_member(user.id, privileges)
    except Exception as e:
        return await Pbxbot.error(message, f"Error demoting user: {e}")

    await Pbxbot.delete(message, f"**🙄 Demoted {user.mention} successfully!**")
    await Pbxbot.check_and_log(
        "demote",
        f"**Demoted User**\n\n**User:** {user.mention}\n**User ID:** `{user.id}`\n**Admin:** {message.from_user.mention}\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`",
    )


@on_message(
    "ban",
    chat_type=group_only,
    admin_only=True,
    allow_stan=True,
    Bad_user=True,
    enable_log=True,
)
@Bad
async def ban(client: Client, message: Message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
        reason = (await Pbxbot.input(message)).strip() if len(message.command) > 1 else None
    elif len(message.command) >= 2:
        user = await client.get_users(message.command[1])
        reason = (await Pbxbot.input(message)).split(" ", 1)[1].strip() if len(message.command) > 2 else None
    else:
        return await Pbxbot.delete(
            message, "Need a username/id or reply to a user to ban them!"
        )

    try:
        await message.chat.ban_member(user.id)
    except Exception as e:
        return await Pbxbot.error(message, f"Error banning user: {e}")

    reason = reason or "Not Specified"
    await Pbxbot.delete(
        message,
        f"**☠️ Banned {user.mention} successfully!**\n**Reason:** `{reason}`",
        30,
    )
    await Pbxbot.check_and_log(
        "ban",
        f"**Banned User**\n\n**User:** {user.mention}\n**User ID:** `{user.id}`\n**Reason:** `{reason}`\n**Admin:** {message.from_user.mention}\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`",
    )


@on_message(
    "unban",
    chat_type=group_only,
    admin_only=True,
    allow_stan=True,
    Bad_user=True,
    enable_log=True,
)
async def unban(client: Client, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await Pbxbot.delete(
            message, "Need a username/id or reply to a user to unban them!"
        )

    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        user = await client.get_users(message.command[1])

    try:
        await message.chat.unban_member(user.id)
    except Exception as e:
        return await Pbxbot.error(message, f"Error unbanning user: {e}")

    await Pbxbot.delete(message, f"**🤗 Unbanned {user.mention} successfully!**", 30)
    await Pbxbot.check_and_log(
        "unban",
        f"**Unbanned User**\n\n**User:** {user.mention}\n**User ID:** `{user.id}`\n**Admin:** {message.from_user.mention}\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`",
    )


@on_message(
    "kick",
    chat_type=group_only,
    admin_only=True,
    allow_stan=True,
    Bad_user=True,
    enable_log=True,
)
@Bad
async def kick(client: Client, message: Message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
        reason = (await Pbxbot.input(message)).strip() if len(message.command) > 1 else None
    elif len(message.command) >= 2:
        user = await client.get_users(message.command[1])
        reason = (await Pbxbot.input(message)).split(" ", 1)[1].strip() if len(message.command) > 2 else None
    else:
        return await Pbxbot.delete(
            message, "Need a username/id or reply to a user to kick them!"
        )

    try:
        await message.chat.ban_member(user.id)
        await asyncio.sleep(5)
        await message.chat.unban_member(user.id)
    except Exception as e:
        return await Pbxbot.error(message, f"Error kicking user: {e}")

    reason = reason or "Not Specified"
    await Pbxbot.delete(
        message,
        f"**👋 Kicked {user.mention} successfully!**\n**Reason:** `{reason}`",
        30,
    )
    await Pbxbot.check_and_log(
        "kick",
        f"**Kicked User**\n\n**User:** {user.mention}\n**User ID:** `{user.id}`\n**Reason:** `{reason}`\n**Admin:** {message.from_user.mention}\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`",
    )


@on_message(
    "mute",
    chat_type=group_only,
    admin_only=True,
    allow_stan=True,
    Bad_user=True,
    enable_log=True,
)
@Bad
async def mute(client: Client, message: Message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
        reason = (await Pbxbot.input(message)).strip() if len(message.command) > 1 else None
    elif len(message.command) >= 2:
        user = await client.get_users(message.command[1])
        reason = (await Pbxbot.input(message)).split(" ", 1)[1].strip() if len(message.command) > 2 else None
    else:
        return await Pbxbot.delete(
            message, "Need a username/id or reply to a user to mute them!"
        )

    try:
        permissions = ChatPermissions(can_send_messages=False)
        await message.chat.restrict_member(user.id, permissions)
    except Exception as e:
        return await Pbxbot.error(message, f"Error muting user: {e}")

    reason = reason or "Not Specified"
    await Pbxbot.delete(
        message,
        f"**🤐 Muted {user.mention} successfully!**\n**Reason:** `{reason}`",
        30,
    )
    await Pbxbot.check_and_log(
        "mute",
        f"**Muted User**\n\n**User:** {user.mention}\n**User ID:** `{user.id}`\n**Reason:** `{reason}`\n**Admin:** {message.from_user.mention}\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`",
    )


@on_message(
    "tmute",
    chat_type=group_only,
    admin_only=True,
    allow_stan=True,
    Bad_user=True,
    enable_log=True,
)
@Bad
async def tmute(client: Client, message: Message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
        input_str = (await Pbxbot.input(message)).strip() if len(message.command) > 1 else None
    elif len(message.command) >= 3:
        user = await client.get_users(message.command[1])
        input_str = (await Pbxbot.input(message)).split(" ", 1)[1].strip()
    else:
        return await Pbxbot.delete(
            message, "Need a username/id or reply to a user and duration to timed-mute them! Example: `tmute @user 30m reason`"
        )

    if not input_str:
        return await Pbxbot.delete(
            message, "Please provide a duration (e.g., 30s, 5m, 1h, 1d) and optional reason!"
        )

    # Parse duration and reason
    duration_str = input_str.split(" ")[0].lower()
    reason = " ".join(input_str.split(" ")[1:]).strip() if len(input_str.split(" ")) > 1 else "Not Specified"

    # Convert duration to seconds
    try:
        unit = duration_str[-1]
        value = int(duration_str[:-1])
        if unit == "s":
            seconds = value
        elif unit == "m":
            seconds = value * 60
        elif unit == "h":
            seconds = value * 3600
        elif unit == "d":
            seconds = value * 86400
        else:
            return await Pbxbot.delete(
                message, "Invalid duration unit! Use s (seconds), m (minutes), h (hours), or d (days)."
            )
    except ValueError:
        return await Pbxbot.delete(
            message, "Invalid duration format! Example: `30m`, `1h`, `2d`."
        )

    if seconds < 30 or seconds > 31536000:  # Min 30 seconds, max 1 year
        return await Pbxbot.delete(
            message, "Duration must be between 30 seconds and 1 year!"
        )

    try:
        until_date = int((datetime.now() + timedelta(seconds=seconds)).timestamp())
        permissions = ChatPermissions(can_send_messages=False)
        await message.chat.restrict_member(user.id, permissions, until_date=until_date)
    except Exception as e:
        return await Pbxbot.error(message, f"Error timed-muting user: {e}")

    await Pbxbot.delete(
        message,
        f"**⏲️ Timed-Muted {user.mention} for {duration_str}!**\n**Reason:** `{reason}`",
        30,
    )
    await Pbxbot.check_and_log(
        "tmute",
        f"**Timed-Muted User**\n\n**User:** {user.mention}\n**User ID:** `{user.id}`\n**Duration:** `{duration_str}`\n**Reason:** `{reason}`\n**Admin:** {message.from_user.mention}\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`",
    )


@on_message(
    "unmute",
    chat_type=group_only,
    admin_only=True,
    allow_stan=True,
    Bad_user=True,
    enable_log=True,
)
async def unmute(client: Client, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await Pbxbot.delete(
            message, "Need a username/id or reply to a user to unmute them!"
        )

    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        user = await client.get_users(message.command[1])

    try:
        permissions = ChatPermissions(can_send_messages=True)
        await message.chat.restrict_member(user.id, permissions)
    except Exception as e:
        return await Pbxbot.error(message, f"Error unmuting user: {e}")

    await Pbxbot.delete(message, f"**😁 Unmuted {user.mention} successfully!**", 30)
    await Pbxbot.check_and_log(
        "unmute",
        f"**Unmuted User**\n\n**User:** {user.mention}\n**User ID:** `{user.id}`\n**Admin:** {message.from_user.mention}\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`",
    )


@on_message(
    "pin",
    chat_type=group_only,
    admin_only=True,
    allow_stan=True,
    Bad_user=True,
    enable_log=True,
)
async def pin(_, message: Message):
    if not message.reply_to_message:
        return await Pbxbot.delete(message, "Need a reply to pin a message!")

    try:
        await message.reply_to_message.pin()
    except Exception as e:
        return await Pbxbot.error(message, f"Error pinning message: {e}")

    await Pbxbot.delete(
        message,
        f"**📌 Pinned [Message]({message.reply_to_message.link}) in {message.chat.title}!**",
        30,
    )
    await Pbxbot.check_and_log(
        "pin",
        f"**Pinned Message**\n\n**Message:** [Click Here]({message.reply_to_message.link})\n**Admin:** {message.from_user.mention}\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`",
    )


@on_message(
    "unpin",
    chat_type=group_only,
    admin_only=True,
    allow_stan=True,
    Bad_user=True,
    enable_log=True,
)
async def unpin(_, message: Message):
    if not message.reply_to_message:
        return await Pbxbot.delete(message, "Need a reply to unpin a message!")

    try:
        await message.reply_to_message.unpin()
    except Exception as e:
        return await Pbxbot.error(message, f"Error unpinning message: {e}")

    await Pbxbot.delete(
        message,
        f"**📌 Unpinned [Message]({message.reply_to_message.link}) in {message.chat.title}!**",
        30,
    )
    await Pbxbot.check_and_log(
        "unpin",
        f"**Unpinned Message**\n\n**Message:** [Click Here]({message.reply_to_message.link})\n**Admin:** {message.from_user.mention}\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`",
    )


@on_message(
    "zombies",
    chat_type=group_only,
    admin_only=True,
    allow_stan=True,
    Bad_user=True,
    enable_log=True,
)
async def zombies(_, message: Message):
    Pbx = await Pbxbot.edit(message, "☠️ Detecting zombies...")
    ded_users = []
    async for member in message.chat.get_members():
        if member.user.is_deleted:
            ded_users.append(member.user.id)

    if not ded_users:
        return await Pbx.edit(
            "🫡 No zombies in this group. **Group's clean AF!**"
        )

    if len(message.command) > 1 and message.command[1].lower() == "clean":
        await Pbx.edit(
            f"☠️ Found {len(ded_users)} zombies... **🔫 Time to purge them!**"
        )
        failed = 0
        success = 0
        for user in ded_users:
            try:
                await message.chat.ban_member(user)
                success += 1
            except Exception as e:
                LOGS.error(f"Error banning zombie {user}: {e}")
                failed += 1

        await Pbx.edit(f"**Purged {success} zombies!**\n`{failed}` holds immunity!")
    else:
        await Pbx.edit(
            f"**☠️ Found {len(ded_users)} zombies!**\n\n__Use__ `{handler}zombies clean` __to kill them!__"
        )


HelpMenu("admin").add(
    "promote", "<username/id/reply> <title>", "Promote a user to admin.", "promote @PbxBad Badmunda"
).add(
    "fullpromote", "<username/id/reply> <title>", "Fully promote a user to admin with all privileges.", "fullpromote @PbxBad SuperAdmin"
).add(
    "demote", "<username/id/reply>", "Demote a user from admin.", "demote @PbxBad"
).add(
    "ban", "<username/id/reply> <reason>", "Ban a user from the group.", "ban @PbxBad Spamming"
).add(
    "unban", "<username/id/reply>", "Unban a user from the group.", "unban @PbxBad"
).add(
    "kick", "<username/id/reply> <reason>", "Kick a user from the group.", "kick @PbxBad Trolling"
).add(
    "mute", "<username/id/reply> <reason>", "Mute a user in the group.", "mute @PbxBad Flooding"
).add(
    "tmute", "<username/id/reply> <duration> <reason>", "Mute a user for a specific duration (e.g., 30s, 5m, 1h, 1d).", "tmute @PbxBad 30m Spamming"
).add(
    "unmute", "<username/id/reply>", "Unmute a user in the group.", "unmute @PbxBad"
).add(
    "pin", "<reply>", "Pin the replied message in the group."
).add(
    "unpin", "<reply>", "Unpin the replied pinned message in the group."
).add(
    "zombies", "clean", "Finds and optionally bans deleted accounts in the group."
).info("Admin Menu").done()
