import asyncio
import datetime
import time

from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait
from pyrogram.types import ChatPermissions, ChatPrivileges, Message

from Pbxbot.functions.templates import (
    gban_templates,
    gwarn_templates,
    gwarn_autoban_templates,
    gtempban_templates,
    gpin_templates,
    gbroadcast_templates,
    gcheck_templates,
    gstats_templates,
    gshadowban_templates,
    gsilence_templates,
    gunsilence_templates,
    gblacklist_templates,
)

from . import Config, HelpMenu, Symbols, custom_handler, db, Pbxbot, on_message
from . import *


@on_message("gpromote", allow_stan=True, Bad_user=True, enable_log=True)
async def globalpromote(client: Client, message: Message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            return await Pbxbot.delete(
                message, "Reply to a user or pass a username/id to gpromote."
            )
        try:
            user = await client.get_users(message.command[1])
        except Exception as e:
            return await Pbxbot.error(message, f"`{str(e)}`")
        reason = (
            message.text.split(None, 2)[2]
            if len(message.text.split()) > 2
            else "No reason provided."
        )
    else:
        user = message.reply_to_message.from_user
        reason = await Pbxbot.input(message) or "No reason provided."

    if user.is_self:
        return await Pbxbot.delete(message, "I can't gpromote myself.")

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

    success = 0
    failed = 0
    Pbx = await Pbxbot.edit(message, f"Gpromote initiated on {user.mention}...")

    async for dialog in client.get_dialogs():
        if dialog.chat.type in [
            ChatType.CHANNEL,
            ChatType.GROUP,
            ChatType.SUPERGROUP,
        ]:
            try:
                await dialog.chat.promote_member(user.id, privileges)
                success += 1
            except FloodWait as e:
                await Pbx.edit(
                    f"Gpromote initiated on {user.mention}...\nSleeping for {e.x} seconds due to floodwait..."
                )
                await asyncio.sleep(e.x)
                try:
                    await dialog.chat.promote_member(user.id, privileges)
                    success += 1
                except BaseException:
                    failed += 1
                await Pbx.edit(f"Gpromote initiated on {user.mention}...")
            except BaseException:
                failed += 1

    await Pbx.edit(
        await gban_templates(
            gtype="𝖦-𝖯𝗋𝗈𝗆𝗈𝗍𝖾",
            name=user.mention,
            success=success,
            failed=failed,
            reason=reason,
        )
    )

    await Pbxbot.check_and_log(
        "gpromote",
        f"**User:** {user.mention} (`{user.id}`)\n**By:** {client.me.mention}\n\n**Reason:** `{reason}`",
    )


@on_message("gdemote", allow_stan=True, Bad_user=True, enable_log=True)
@Bad
@special
async def globaldemote(client: Client, message: Message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            return await Pbxbot.delete(
                message, "Reply to a user or pass a username/id to gdemote."
            )
        try:
            user = await client.get_users(message.command[1])
        except Exception as e:
            return await Pbxbot.error(message, f"`{str(e)}`")
        reason = (
            message.text.split(None, 2)[2]
            if len(message.text.split()) > 2
            else "No reason provided."
        )
    else:
        user = message.reply_to_message.from_user
        reason = await Pbxbot.input(message) or "No reason provided."

    if user.is_self:
        return await Pbxbot.delete(message, "I can't gdemote myself.")

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

    success = 0
    failed = 0
    Pbx = await Pbxbot.edit(message, f"Gdemote initiated on {user.mention}...")

    async for dialog in client.get_dialogs():
        if dialog.chat.type in [
            ChatType.CHANNEL,
            ChatType.GROUP,
            ChatType.SUPERGROUP,
        ]:
            try:
                await dialog.chat.promote_member(user.id, privileges)
                success += 1
            except FloodWait as e:
                await Pbx.edit(
                    f"Gdemote initiated on {user.mention}...\nSleeping for {e.x} seconds due to floodwait..."
                )
                await asyncio.sleep(e.x)
                try:
                    await dialog.chat.promote_member(user.id, privileges)
                    success += 1
                except BaseException:
                    failed += 1
                await Pbx.edit(f"Gdemote initiated on {user.mention}...")
            except BaseException:
                failed += 1

    await Pbx.edit(
        await gban_templates(
            gtype="𝖦-𝖣𝖾𝗆𝗈𝗍𝖾",
            name=user.mention,
            success=success,
            failed=failed,
            reason=reason,
        )
    )

    await Pbxbot.check_and_log(
        "gdemote",
        f"**User:** {user.mention} (`{user.id}`)\n**By:** {client.me.mention}\n\n**Reason:** `{reason}`",
    )


@on_message("gban", allow_stan=True, Bad_user=True, enable_log=True)
@Bad
@special
async def globalban(client: Client, message: Message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            return await Pbxbot.delete(
                message, "Reply to a user or pass a username/id to gban."
            )
        try:
            user = await client.get_users(message.command[1])
        except Exception as e:
            return await Pbxbot.error(message, f"`{str(e)}`")
        reason = (
            message.text.split(None, 2)[2]
            if len(message.text.split()) > 2
            else "No reason provided."
        )
    else:
        user = message.reply_to_message.from_user
        reason = await Pbxbot.input(message) or "No reason provided."

    if user.is_self:
        return await Pbxbot.delete(message, "I can't gban myself.")

    if user.id in Config.AUTH_USERS:
        return await Pbxbot.delete(message, "I can't gban my auth user.")

    if await db.is_gbanned(user.id, client.me.id):
        return await Pbxbot.delete(message, "This user is already gbanned.")

    if user.id in Config.DEVS:
        return await Pbxbot.delete(message, "I can't gban my devs.")

    success = 0
    failed = 0
    Pbx = await Pbxbot.edit(message, f"Gban initiated on {user.mention}...")

    await db.add_gban(user.id, reason, client.me.id)
    

    async for dialog in client.get_dialogs():
        if dialog.chat.type in [
            ChatType.CHANNEL,
            ChatType.GROUP,
            ChatType.SUPERGROUP,
        ]:
            try:
                await dialog.chat.ban_member(user.id)
                success += 1
            except FloodWait as e:
                await Pbx.edit(
                    f"Gban initiated on {user.mention}...\nSleeping for {e.x} seconds due to floodwait..."
                )
                await asyncio.sleep(e.x)
                await dialog.chat.ban_member(user.id)
                success += 1
                await Pbx.edit(f"Gban initiated on {user.mention}...")
            except BaseException:
                failed += 1

    await Pbx.edit(
        await gban_templates(
            gtype="𝖦-𝖡𝖺𝗇",
            name=user.mention,
            success=success,
            failed=failed,
            reason=reason,
        )
    )

    await Pbxbot.check_and_log(
        "gban",
        f"**User:** {user.mention} (`{user.id}`)\n**By:** {client.me.mention}\n\n**Reason:** `{reason}`",
    )


@on_message("ungban", allow_stan=True, Bad_user=True, enable_log=True)
async def unglobalban(client: Client, message: Message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            return await Pbxbot.delete(
                message, "Reply to a user or pass a username/id to ungban."
            )
        try:
            user = await client.get_users(message.command[1])
        except Exception as e:
            return await Pbxbot.error(message, f"`{str(e)}`")
    else:
        user = message.reply_to_message.from_user

    if not await db.is_gbanned(user.id, client.me.id):
        await Pbxbot.delete(
            message,
            "This user is not gbanned. Unbanning in all my admin chats anyway...",
        )
    else:
        reason = await db.rm_gban(user.id, client.me.id)
        
        await Pbxbot.edit(
            message,
            f"**𝖴𝗇𝗀𝖻𝖺𝗇𝗇𝖾𝖽** {user.mention}!\n\n**𝖦𝖻𝖺𝗇 𝖱𝖾𝖺𝗌𝗈𝗇 𝗐𝖺𝗌:** `{reason}`",
        )

    async for dialog in client.get_dialogs():
        if dialog.chat.type in [
            ChatType.CHANNEL,
            ChatType.GROUP,
            ChatType.SUPERGROUP,
        ]:
            try:
                await dialog.chat.unban_member(user.id)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await dialog.chat.unban_member(user.id)
            except BaseException:
                pass

    await Pbxbot.check_and_log(
        "ungban",
        f"**User:** {user.mention} (`{user.id}`)\n**By:** {message.from_user.mention}",
    )


@on_message("gkick", allow_stan=True, Bad_user=True, enable_log=True)
@Bad
@special
async def globalkick(client: Client, message: Message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            return await Pbxbot.delete(
                message, "Reply to a user or pass a username/id to gkick."
            )
        try:
            user = await client.get_users(message.command[1])
        except Exception as e:
            return await Pbxbot.error(message, f"`{str(e)}`")
        reason = (
            message.text.split(None, 2)[2]
            if len(message.text.split()) > 2
            else "No reason provided."
        )
    else:
        user = message.reply_to_message.from_user
        reason = await Pbxbot.input(message) or "No reason provided."

    if user.is_self:
        return await Pbxbot.delete(message, "I can't gmute myself.")

    if user.id in Config.AUTH_USERS:
        return await Pbxbot.delete(message, "I can't gmute my auth user.")

    if await db.is_gbanned(user.id, client.me.id):
        return await Pbxbot.delete(
            message, "This user is already gbanned. There's no point in kicking them!"
        )

    if user.id in Config.DEVS:
        return await Pbxbot.delete(message, "I can't gkick my devs.")

    success = 0
    failed = 0
    Pbx = await Pbxbot.edit(message, f"Gkick initiated on {user.mention}...")

    async for dialog in client.get_dialogs():
        if dialog.chat.type in [
            ChatType.CHANNEL,
            ChatType.GROUP,
            ChatType.SUPERGROUP,
        ]:
            try:
                await dialog.chat.ban_member(
                    user.id, datetime.datetime.now() + datetime.timedelta(seconds=35)
                )
                success += 1
            except FloodWait as e:
                await Pbx.edit(
                    f"Gkick initiated on {user.mention}...\nSleeping for {e.x} seconds due to floodwait..."
                )
                await asyncio.sleep(e.x)
                await dialog.chat.ban_member(
                    user.id, datetime.datetime.now() + datetime.timedelta(seconds=35)
                )
                success += 1
                await Pbx.edit(f"Gkick initiated on {user.mention}...")
            except BaseException:
                failed += 1

    await Pbx.edit(
        await gban_templates(
            gtype="𝖦-𝖪𝗂𝖼𝗄",
            name=user.mention,
            success=success,
            failed=failed,
            reason=reason,
        )
    )

    await Pbxbot.check_and_log(
        "gkick",
        f"**User:** {user.mention} (`{user.id}`)\n**By:** {client.me.mention}\n\n**Reason:** `{reason}`",
    )


@on_message("gmute", allow_stan=True, Bad_user=True, enable_log=True)
@Bad
@special
async def globalmute(client: Client, message: Message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            return await Pbxbot.delete(
                message, "Reply to a user or pass a username/id to gmute."
            )
        try:
            user = await client.get_users(message.command[1])
        except Exception as e:
            return await Pbxbot.error(message, f"`{str(e)}`")
        reason = (
            message.text.split(None, 2)[2]
            if len(message.text.split()) > 2
            else "No reason provided."
        )
    else:
        user = message.reply_to_message.from_user
        reason = await Pbxbot.input(message) or "No reason provided."

    if user.is_self:
        return await Pbxbot.delete(message, "I can't gmute myself.")

    if user.id in Config.AUTH_USERS:
        return await Pbxbot.delete(message, "I can't gmute my auth user.")

    if await db.is_gmuted(user.id, client.me.id):
        return await Pbxbot.delete(message, "This user is already gmuted.")

    if user.id in Config.DEVS:
        return await Pbxbot.delete(message, "I can't gmute my devs.")

    permissions = ChatPermissions(can_send_messages=False)
    success = 0
    failed = 0
    Pbx = await Pbxbot.edit(message, f"Gmute initiated on {user.mention}...")

    await db.add_gmute(user.id, reason, client.me.id)
    

    async for dialog in client.get_dialogs():
        if dialog.chat.type in [
            ChatType.CHANNEL,
            ChatType.GROUP,
            ChatType.SUPERGROUP,
        ]:
            try:
                await dialog.chat.restrict_member(user.id, permissions)
                success += 1
            except FloodWait as e:
                await Pbx.edit(
                    f"Gmute initiated on {user.mention}...\nSleeping for {e.x} seconds due to floodwait..."
                )
                await asyncio.sleep(e.x)
                await dialog.chat.restrict_member(user.id, permissions)
                success += 1
                await Pbx.edit(f"Gmute initiated on {user.mention}...")
            except BaseException:
                failed += 1

    await Pbx.edit(
        await gban_templates(
            gtype="𝖦-𝖬𝗎𝗍𝖾",
            name=user.mention,
            success=success,
            failed=failed,
            reason=reason,
        )
    )

    await Pbxbot.check_and_log(
        "gmute",
        f"**User:** {user.mention} (`{user.id}`)\n**By:** {client.me.mention}\n\n**Reason:** `{reason}`",
    )


@on_message("ungmute", allow_stan=True, Bad_user=True, enable_log=True)
async def unglobalmute(client: Client, message: Message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            return await Pbxbot.delete(
                message, "Reply to a user or pass a username/id to ungmute."
            )
        try:
            user = await client.get_users(message.command[1])
        except Exception as e:
            return await Pbxbot.error(message, f"`{str(e)}`")
    else:
        user = message.reply_to_message.from_user

    if not await db.is_gmuted(user.id, client.me.id):
        await Pbxbot.delete(
            message, "This user is not gmuted. Unmuting in all my admin chats anyway..."
        )
    else:
        reason = await db.rm_gmute(user.id, client.me.id)
        
        await Pbxbot.edit(
            message,
            f"**𝖴𝗇𝗀𝗆𝗎𝗍𝖾𝖽** {user.mention}!\n\n**𝖦𝗆𝗎𝗍𝖾 𝖱𝖾𝖺𝗌𝗈𝗇 𝗐𝖺𝗌:** `{reason}`",
        )

    permissions = ChatPermissions(can_send_messages=True)

    async for dialog in client.get_dialogs():
        if dialog.chat.type in [
            ChatType.CHANNEL,
            ChatType.GROUP,
            ChatType.SUPERGROUP,
        ]:
            try:
                await dialog.chat.restrict_member(user.id, permissions)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await dialog.chat.restrict_member(user.id, permissions)
            except BaseException:
                pass

    await Pbxbot.check_and_log(
        "ungmute",
        f"**User:** {user.mention} (`{user.id}`)\n**By:** {message.from_user.mention}",
    )


@on_message("gbanlist", allow_stan=True, Bad_user=True, enable_log=True)
async def gbanlist(client: Client, message: Message):
    gban_users = await db.get_gban(client.me.id)
    if not gban_users:
        return await Pbxbot.delete(message, "No gbanned users.")

    Pbx = await Pbxbot.edit(message, "Fetching gbanned users...")
    text = f"**💥 𝖦𝖻𝖺𝗇𝗇𝖾𝖽 𝖴𝗌𝖾𝗋𝗌:** __{len(gban_users)}__\n\n"

    for user in gban_users:
        text += f"{Symbols.bullet} `{user['user_id']}` | __{user['reason']}__\n\n"

    await Pbx.edit(text)


@on_message("gmutelist", allow_stan=True, Bad_user=True, enable_log=True)
async def gmutelist(client: Client, message: Message):
    gmute_users = await db.get_gmute(client.me.id)
    if not gmute_users:
        return await Pbxbot.delete(message, "No gmuted users.")

    Pbx = await Pbxbot.edit(message, "Fetching gmuted users...")
    text = f"**😶 𝖦𝗆𝗎𝗍𝖾𝖽 𝖴𝗌𝖾𝗋𝗌:** __{len(gmute_users)}__\n\n"

    for user in gmute_users:
        text += f"{Symbols.bullet} `{user['user_id']}` | __{user['reason']}__\n\n"

    await Pbx.edit(text)


@custom_handler(filters.incoming & ~filters.service)
async def globalmutewatcher(client, message: Message):
    if not message.from_user:
        return
    if await db.is_gmuted(message.from_user.id, client.me.id):
        try:
            await message.delete()
        except BaseException:
            pass


@custom_handler(filters.new_chat_members)
async def globalbanwatcher(client, message: Message):
    if not message.from_user:
        return
    if await db.is_gbanned(message.from_user.id, client.me.id):
        gban_data = await db.get_gban_user(message.from_user.id, client.me.id)
        watchertext = (
            f"**𝖦𝖻𝖺𝗇𝗇𝖾𝖽 𝖴𝗌𝖾𝗋 𝗃𝗈𝗂𝗇𝖾𝖽 𝗍𝗁𝖾 𝖼𝗁𝖺𝗍!\n\n"
            f"{Symbols.bullet} 𝖦𝖻𝖺𝗇 𝖱𝖾𝖺𝗌𝗈𝗇 𝗐𝖺𝗌:** __{gban_data['reason']}__\n"
            f"**{Symbols.bullet} 𝖦𝖻𝖺𝗇 𝖣𝖺𝗍𝖾:** __{gban_data['date']}__\n\n"
        )
        try:
            await message.chat.ban_member(message.from_user.id)
            watchertext += "**𝖲𝗈𝗋𝗋𝗒 𝖨 𝖼𝖺𝗇'𝗍 𝗌𝖾𝖾 𝗒𝗈𝗎 𝗂𝗇 𝗍𝗁𝗂𝗌 𝖼𝗁𝖺𝗍!**"
        except BaseException:
            watchertext += "Reported to @admins"
        await message.reply_text(watchertext)



# ══════════════════════════════════════════════════════
#  ⚠️  GWARN / UNGWARN / GWARNLIST
# ══════════════════════════════════════════════════════

@on_message("gwarn", allow_stan=True, Bad_user=True, enable_log=True)
@Bad
@special
async def globalwarn(client: Client, message: Message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            return await Pbxbot.delete(
                message, "Reply to a user or pass a username/id to gwarn."
            )
        try:
            user = await client.get_users(message.command[1])
        except Exception as e:
            return await Pbxbot.error(message, f"`{str(e)}`")
        reason = (
            message.text.split(None, 2)[2]
            if len(message.text.split()) > 2
            else "No reason provided."
        )
    else:
        user = message.reply_to_message.from_user
        reason = await Pbxbot.input(message) or "No reason provided."

    if user.is_self:
        return await Pbxbot.delete(message, "I can't gwarn myself.")
    if user.id in Config.AUTH_USERS:
        return await Pbxbot.delete(message, "I can't gwarn my auth user.")
    if user.id in Config.DEVS:
        return await Pbxbot.delete(message, "I can't gwarn my devs.")
    if await db.is_gbanned(user.id, client.me.id):
        return await Pbxbot.delete(message, "User is already gbanned — no need to warn.")

    warn_count = await db.add_gwarn(user.id, reason, client.me.id)
    WARN_LIMIT = db.GWARN_LIMIT

    if warn_count >= WARN_LIMIT:
        await db.add_gban(user.id, f"Auto-GBan: {WARN_LIMIT} global warns reached.", client.me.id)
        
        success, failed = 0, 0
        Pbx = await Pbxbot.edit(
            message,
            f"⚠️ {user.mention} hit **{WARN_LIMIT}/{WARN_LIMIT} warns!**\n🔨 Auto-GBan initiated..."
        )
        async for dialog in client.get_dialogs():
            if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP, ChatType.CHANNEL]:
                try:
                    await dialog.chat.ban_member(user.id)
                    success += 1
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await dialog.chat.ban_member(user.id)
                    success += 1
                except BaseException:
                    failed += 1
        await Pbx.edit(
            await gwarn_autoban_templates(
                name=user.mention,
                warn_limit=WARN_LIMIT,
                success=success,
                failed=failed,
            )
        )
    else:
        await Pbxbot.edit(
            message,
            await gwarn_templates(
                name=user.mention,
                warn_count=warn_count,
                warn_limit=WARN_LIMIT,
                reason=reason,
            )
        )

    await Pbxbot.check_and_log(
        "gwarn",
        f"**User:** {user.mention} (`{user.id}`)\n**By:** {client.me.mention}\n"
        f"**Warns:** `{warn_count}/{WARN_LIMIT}`\n**Reason:** `{reason}`",
    )


@on_message("ungwarn", allow_stan=True, Bad_user=True, enable_log=True)
async def unglobalwarn(client: Client, message: Message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            return await Pbxbot.delete(
                message, "Reply to a user or pass a username/id to ungwarn."
            )
        try:
            user = await client.get_users(message.command[1])
        except Exception as e:
            return await Pbxbot.error(message, f"`{str(e)}`")
    else:
        user = message.reply_to_message.from_user

    if not await db.is_gwarned(user.id, client.me.id):
        return await Pbxbot.delete(message, f"{user.mention} has no active global warns.")

    prev_count = await db.rm_gwarn(user.id, client.me.id)
    await Pbxbot.edit(
        message,
        f"✅ **Global warns cleared** for {user.mention}!\n"
        f"{Symbols.bullet} **Previous warns:** `{prev_count}`"
    )
    await Pbxbot.check_and_log(
        "ungwarn",
        f"**User:** {user.mention} (`{user.id}`)\n**By:** {message.from_user.mention}",
    )


@on_message("gwarnlist", allow_stan=True, Bad_user=True, enable_log=True)
async def gwarnlist(client: Client, message: Message):
    warned = await db.get_all_gwarns(client.me.id)
    if not warned:
        return await Pbxbot.delete(message, "No globally warned users.")
    Pbx = await Pbxbot.edit(message, "Fetching gwarn list...")
    text = f"**⚠️ 𝖦𝗐𝖺𝗋𝗇𝖾𝖽 𝖴𝗌𝖾𝗋𝗌:** __{len(warned)}__\n\n"
    for u in warned:
        latest = u["warns"][-1]["reason"] if u.get("warns") else "Unknown"
        text += f"{Symbols.bullet} `{u['user_id']}` | **{u['count']}/{db.GWARN_LIMIT} warns** | __{latest}__\n\n"
    await Pbx.edit(text)


# ══════════════════════════════════════════════════════
#  ⏳  GTEMPBAN
# ══════════════════════════════════════════════════════

@on_message("gtempban", allow_stan=True, Bad_user=True, enable_log=True)
@Bad
@special
async def globaltempban(client: Client, message: Message):
    if not message.reply_to_message:
        if len(message.command) < 3:
            return await Pbxbot.delete(
                message, "Usage: `.gtempban <reply/user> <time: 1h/30m/2d> <reason>`"
            )
        try:
            user = await client.get_users(message.command[1])
        except Exception as e:
            return await Pbxbot.error(message, f"`{str(e)}`")
        time_str = message.command[2]
        reason = (
            message.text.split(None, 3)[3]
            if len(message.text.split()) > 3
            else "No reason provided."
        )
    else:
        if len(message.command) < 2:
            return await Pbxbot.delete(message, "Please provide a time duration. e.g. `1h`, `30m`, `2d`")
        user = message.reply_to_message.from_user
        time_str = message.command[1]
        reason = (
            message.text.split(None, 2)[2]
            if len(message.text.split()) > 2
            else "No reason provided."
        )

    if user.is_self:
        return await Pbxbot.delete(message, "I can't gtempban myself.")
    if user.id in Config.AUTH_USERS:
        return await Pbxbot.delete(message, "I can't gtempban my auth user.")
    if user.id in Config.DEVS:
        return await Pbxbot.delete(message, "I can't gtempban my devs.")

    time_map = {"m": 60, "h": 3600, "d": 86400}
    try:
        unit = time_str[-1].lower()
        amount = int(time_str[:-1])
        if unit not in time_map or amount <= 0:
            raise ValueError
        seconds = amount * time_map[unit]
    except (ValueError, IndexError):
        return await Pbxbot.delete(message, "Invalid time format! Use: `30m`, `2h`, `1d`")

    until_date = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
    success, failed = 0, 0
    Pbx = await Pbxbot.edit(message, f"⏳ GTempBan on {user.mention} for `{time_str}`...")

    async for dialog in client.get_dialogs():
        if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP, ChatType.CHANNEL]:
            try:
                await dialog.chat.ban_member(user.id, until_date=until_date)
                success += 1
            except FloodWait as e:
                await Pbx.edit(f"⏳ GTempBan...\nSleeping {e.x}s (FloodWait)...")
                await asyncio.sleep(e.x)
                await dialog.chat.ban_member(user.id, until_date=until_date)
                success += 1
                await Pbx.edit(f"⏳ GTempBan on {user.mention} for `{time_str}`...")
            except BaseException:
                failed += 1

    await Pbx.edit(
        await gtempban_templates(
            name=user.mention, duration=time_str, success=success, failed=failed, reason=reason
        )
    )
    await Pbxbot.check_and_log(
        "gtempban",
        f"**User:** {user.mention} (`{user.id}`)\n**By:** {client.me.mention}\n"
        f"**Duration:** `{time_str}`\n**Reason:** `{reason}`",
    )


# ══════════════════════════════════════════════════════
#  📌  GPIN
# ══════════════════════════════════════════════════════

@on_message("gpin", allow_stan=True, Bad_user=True, enable_log=True)
async def globalpin(client: Client, message: Message):
    if not message.reply_to_message:
        return await Pbxbot.delete(message, "Reply to a message to globally pin it.")

    pin_text = (
        message.reply_to_message.text
        or message.reply_to_message.caption
        or "📌 Pinned Message"
    )
    success, failed = 0, 0
    Pbx = await Pbxbot.edit(message, "📌 GPin initiated across all chats...")

    async for dialog in client.get_dialogs():
        if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP, ChatType.CHANNEL]:
            try:
                sent = await client.send_message(dialog.chat.id, pin_text)
                await client.pin_chat_message(dialog.chat.id, sent.id, disable_notification=True)
                success += 1
            except FloodWait as e:
                await Pbx.edit(f"📌 GPin...\nSleeping {e.x}s (FloodWait)...")
                await asyncio.sleep(e.x)
                try:
                    sent = await client.send_message(dialog.chat.id, pin_text)
                    await client.pin_chat_message(dialog.chat.id, sent.id, disable_notification=True)
                    success += 1
                except BaseException:
                    failed += 1
            except BaseException:
                failed += 1

    await Pbx.edit(await gpin_templates(success=success, failed=failed))
    await Pbxbot.check_and_log(
        "gpin",
        f"**By:** {client.me.mention}\n**Pinned in:** `{success}` chats | **Failed:** `{failed}`",
    )


# ══════════════════════════════════════════════════════
#  📢  GBROADCAST
# ══════════════════════════════════════════════════════

@on_message("gbroadcast", allow_stan=True, Bad_user=True, enable_log=True)
async def globalbroadcast(client: Client, message: Message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            return await Pbxbot.delete(
                message, "Reply to a message OR write text after `.gbroadcast`."
            )
        text = message.text.split(None, 1)[1]
    else:
        text = message.reply_to_message.text or message.reply_to_message.caption
        if not text:
            return await Pbxbot.delete(message, "Replied message has no text to broadcast.")

    success, failed, total = 0, 0, 0
    start_time = time.time()
    Pbx = await Pbxbot.edit(message, "📢 GBroadcast initiated...")

    async for dialog in client.get_dialogs():
        if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP, ChatType.CHANNEL]:
            total += 1
            try:
                await client.send_message(dialog.chat.id, text)
                success += 1
            except FloodWait as e:
                await Pbx.edit(f"📢 GBroadcast...\nSleeping {e.x}s (FloodWait)...")
                await asyncio.sleep(e.x)
                try:
                    await client.send_message(dialog.chat.id, text)
                    success += 1
                except BaseException:
                    failed += 1
            except BaseException:
                failed += 1

    elapsed = round(time.time() - start_time, 2)
    await Pbx.edit(
        await gbroadcast_templates(success=success, failed=failed, total=total, time_taken=f"{elapsed}s")
    )
    await Pbxbot.check_and_log(
        "gbroadcast",
        f"**By:** {client.me.mention}\n**Sent:** `{success}/{total}`\n**Time:** `{elapsed}s`",
    )


# ══════════════════════════════════════════════════════
#  🔍  GCHECK
# ══════════════════════════════════════════════════════

@on_message("gcheck", allow_stan=True, Bad_user=True, enable_log=True)
async def globalcheck(client: Client, message: Message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            return await Pbxbot.delete(
                message, "Reply to a user or pass a username/id to gcheck."
            )
        try:
            user = await client.get_users(message.command[1])
        except Exception as e:
            return await Pbxbot.error(message, f"`{str(e)}`")
    else:
        user = message.reply_to_message.from_user

    is_gbanned  = await db.is_gbanned(user.id, client.me.id)
    is_gmuted   = await db.is_gmuted(user.id, client.me.id)
    warn_count  = await db.get_gwarn_count(user.id, client.me.id)
    is_shadow   = await db.is_gshadowbanned(client.me.id, user.id)
    is_silenced = await db.is_gsilenced(client.me.id, user.id)
    credits     = await db.get_credits(user.id)

    if user.id in Config.DEVS:
        role = "👑 **Dev**"
    elif user.id in Config.AUTH_USERS:
        role = "🔑 **Auth User**"
    elif is_gbanned:
        role = "🔨 **GBanned**"
    else:
        role = "👤 User"

    await Pbxbot.edit(
        message,
        await gcheck_templates(
            mention=user.mention,
            user_id=user.id,
            gban_status="🔨 `Yes`" if is_gbanned else "✅ `No`",
            gmute_status="🔇 `Yes`" if is_gmuted else "✅ `No`",
            gwarn_status=f"⚠️ `{warn_count}/3`" if warn_count > 0 else "✅ `0/3`",
            shadow_status="👻 `Yes`" if is_shadow else "✅ `No`",
            silence_status="🔕 `Yes`" if is_silenced else "✅ `No`",
            credits=credits,
            role=role,
        )
    )


# ══════════════════════════════════════════════════════
#  📊  GSTATS
# ══════════════════════════════════════════════════════

@on_message("gstats", allow_stan=True, Bad_user=True, enable_log=True)
async def globalstats(client: Client, message: Message):
    Pbx = await Pbxbot.edit(message, "📊 Fetching global stats...")
    groups, channels = 0, 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            groups += 1
        elif dialog.chat.type == ChatType.CHANNEL:
            channels += 1

    await Pbx.edit(
        await gstats_templates(
            groups=groups,
            channels=channels,
            gbans=len(await db.get_gban(client.me.id)),
            gmutes=len(await db.get_gmute(client.me.id)),
            gwarns=len(await db.get_all_gwarns(client.me.id)),
            gshadowbans=len(await db.get_all_gshadowbans(client.me.id)),
            gsilenced=len(await db.get_all_gsilenced(client.me.id)),
            gblacklists=len(await db.get_all_gblacklists()),
            total=groups + channels,
        )
    )


# ══════════════════════════════════════════════════════
#  👻  GSHADOWBAN / UNGSHADOWBAN
# ══════════════════════════════════════════════════════

@on_message("gshadowban", allow_stan=True, Bad_user=True, enable_log=True)
@Bad
@special
async def globalshadowban(client: Client, message: Message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            return await Pbxbot.delete(
                message, "Reply to a user or pass a username/id to gshadowban."
            )
        try:
            user = await client.get_users(message.command[1])
        except Exception as e:
            return await Pbxbot.error(message, f"`{str(e)}`")
        reason = (
            message.text.split(None, 2)[2]
            if len(message.text.split()) > 2
            else "No reason provided."
        )
    else:
        user = message.reply_to_message.from_user
        reason = await Pbxbot.input(message) or "No reason provided."

    if user.is_self:
        return await Pbxbot.delete(message, "I can't gshadowban myself.")
    if user.id in Config.AUTH_USERS:
        return await Pbxbot.delete(message, "I can't gshadowban my auth user.")
    if user.id in Config.DEVS:
        return await Pbxbot.delete(message, "I can't gshadowban my devs.")
    if await db.is_gshadowbanned(client.me.id, user.id):
        return await Pbxbot.delete(message, "This user is already gshadowbanned.")

    await db.add_gshadowban(client.me.id, user.id, reason)
    permissions = ChatPermissions(can_send_messages=False)
    success, failed = 0, 0
    Pbx = await Pbxbot.edit(message, f"👻 GShadowBan initiated on {user.mention}...")

    async for dialog in client.get_dialogs():
        if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            try:
                await dialog.chat.restrict_member(user.id, permissions)
                success += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                try:
                    await dialog.chat.restrict_member(user.id, permissions)
                    success += 1
                except BaseException:
                    failed += 1
            except BaseException:
                failed += 1

    await Pbx.edit(await gshadowban_templates(name=user.mention, success=success, failed=failed, reason=reason))
    await Pbxbot.check_and_log(
        "gshadowban",
        f"**User:** {user.mention} (`{user.id}`)\n**By:** {client.me.mention}\n**Reason:** `{reason}`",
    )


@on_message("ungshadowban", allow_stan=True, Bad_user=True, enable_log=True)
async def unglobalshadowban(client: Client, message: Message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            return await Pbxbot.delete(
                message, "Reply to a user or pass a username/id to ungshadowban."
            )
        try:
            user = await client.get_users(message.command[1])
        except Exception as e:
            return await Pbxbot.error(message, f"`{str(e)}`")
    else:
        user = message.reply_to_message.from_user

    if not await db.is_gshadowbanned(client.me.id, user.id):
        return await Pbxbot.delete(message, "This user is not gshadowbanned.")

    reason = await db.rm_gshadowban(client.me.id, user.id)
    permissions = ChatPermissions(can_send_messages=True)
    async for dialog in client.get_dialogs():
        if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            try:
                await dialog.chat.restrict_member(user.id, permissions)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await dialog.chat.restrict_member(user.id, permissions)
            except BaseException:
                pass

    await Pbxbot.edit(
        message,
        f"✅ **GShadowBan removed** for {user.mention}!\n"
        f"{Symbols.bullet} **Previous reason:** `{reason}`"
    )
    await Pbxbot.check_and_log(
        "ungshadowban",
        f"**User:** {user.mention} (`{user.id}`)\n**By:** {message.from_user.mention}",
    )


# ══════════════════════════════════════════════════════
#  🔕  GSILENCE / UNSILENCE
# ══════════════════════════════════════════════════════

@on_message("gsilence", allow_stan=True, Bad_user=True, enable_log=True)
@Bad
@special
async def globalsilence(client: Client, message: Message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            return await Pbxbot.delete(
                message, "Reply to a user or pass a username/id to gsilence."
            )
        try:
            user = await client.get_users(message.command[1])
        except Exception as e:
            return await Pbxbot.error(message, f"`{str(e)}`")
        reason = (
            message.text.split(None, 2)[2]
            if len(message.text.split()) > 2
            else "No reason provided."
        )
    else:
        user = message.reply_to_message.from_user
        reason = await Pbxbot.input(message) or "No reason provided."

    if user.is_self:
        return await Pbxbot.delete(message, "I can't gsilence myself.")
    if user.id in Config.AUTH_USERS:
        return await Pbxbot.delete(message, "I can't gsilence my auth user.")
    if user.id in Config.DEVS:
        return await Pbxbot.delete(message, "I can't gsilence my devs.")
    if await db.is_gsilenced(client.me.id, user.id):
        return await Pbxbot.delete(message, "This user is already gsilenced.")

    await db.add_gsilence(client.me.id, user.id, reason)
    permissions = ChatPermissions(
        can_send_messages=False,
        can_send_media_messages=False,
        can_send_other_messages=False,
        can_send_polls=False,
        can_add_web_page_previews=False,
        can_change_info=False,
        can_invite_users=False,
        can_pin_messages=False,
    )
    success, failed = 0, 0
    Pbx = await Pbxbot.edit(message, f"🔕 GSilence initiated on {user.mention}...")

    async for dialog in client.get_dialogs():
        if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            try:
                await dialog.chat.restrict_member(user.id, permissions)
                success += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                try:
                    await dialog.chat.restrict_member(user.id, permissions)
                    success += 1
                except BaseException:
                    failed += 1
            except BaseException:
                failed += 1

    await Pbx.edit(await gsilence_templates(name=user.mention, success=success, failed=failed, reason=reason))
    await Pbxbot.check_and_log(
        "gsilence",
        f"**User:** {user.mention} (`{user.id}`)\n**By:** {client.me.mention}\n**Reason:** `{reason}`",
    )


@on_message("unsilence", allow_stan=True, Bad_user=True, enable_log=True)
async def unglobalsilence(client: Client, message: Message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            return await Pbxbot.delete(
                message, "Reply to a user or pass a username/id to unsilence."
            )
        try:
            user = await client.get_users(message.command[1])
        except Exception as e:
            return await Pbxbot.error(message, f"`{str(e)}`")
    else:
        user = message.reply_to_message.from_user

    if not await db.is_gsilenced(client.me.id, user.id):
        return await Pbxbot.delete(message, "This user is not gsilenced.")

    reason = await db.rm_gsilence(client.me.id, user.id)
    permissions = ChatPermissions(
        can_send_messages=True, can_send_media_messages=True,
        can_send_other_messages=True, can_send_polls=True,
        can_add_web_page_previews=True, can_invite_users=True,
    )
    success, failed = 0, 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            try:
                await dialog.chat.restrict_member(user.id, permissions)
                success += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await dialog.chat.restrict_member(user.id, permissions)
                success += 1
            except BaseException:
                failed += 1

    await Pbxbot.edit(message, await gunsilence_templates(name=user.mention, success=success, failed=failed))
    await Pbxbot.check_and_log(
        "unsilence",
        f"**User:** {user.mention} (`{user.id}`)\n**By:** {message.from_user.mention}",
    )


# ══════════════════════════════════════════════════════
#  🚫  GBLACKLIST / UNGBLACKLIST / GBLACKLISTS
# ══════════════════════════════════════════════════════

@on_message("gblacklist", allow_stan=True, Bad_user=True, enable_log=True)
async def add_globalblacklist(client: Client, message: Message):
    if len(message.command) < 2:
        return await Pbxbot.delete(message, "Usage: `.gblacklist <word>`")
    word = message.command[1].lower()
    if await db.is_gblacklisted(word):
        return await Pbxbot.delete(message, f"`{word}` is already globally blacklisted.")
    await db.add_gblacklist(word)
    groups = sum(1 async for d in client.get_dialogs() if d.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP])
    await Pbxbot.edit(message, await gblacklist_templates(word=word, groups=groups))
    await Pbxbot.check_and_log("gblacklist", f"**Word:** `{word}`\n**By:** {client.me.mention}\n**Active in:** `{groups}` groups")


@on_message("ungblacklist", allow_stan=True, Bad_user=True, enable_log=True)
async def rm_globalblacklist(client: Client, message: Message):
    if len(message.command) < 2:
        return await Pbxbot.delete(message, "Usage: `.ungblacklist <word>`")
    word = message.command[1].lower()
    if not await db.is_gblacklisted(word):
        return await Pbxbot.delete(message, f"`{word}` is not in global blacklist.")
    await db.rm_gblacklist(word)
    await Pbxbot.edit(message, f"✅ `{word}` removed from global blacklist!")
    await Pbxbot.check_and_log("ungblacklist", f"**Word:** `{word}`\n**By:** {client.me.mention}")


@on_message("gblacklists", allow_stan=True, Bad_user=True, enable_log=True)
async def list_globalblacklist(_, message: Message):
    words = await db.get_all_gblacklists()
    if not words:
        return await Pbxbot.delete(message, "No words in global blacklist.")
    Pbx = await Pbxbot.edit(message, "Fetching global blacklist...")
    text = f"**🚫 𝖦𝗅𝗈𝖻𝖺𝗅 𝖡𝗅𝖺𝖼𝗄𝗅𝗂𝗌𝗍 ({len(words)} words):**\n\n"
    for w in words:
        text += f"{Symbols.bullet} `{w['word']}` — __{w['date']}__\n"
    await Pbx.edit(text)



# ══════════════════════════════════════════════════════
#  👁️  WATCHERS — auto-enforce silently
# ══════════════════════════════════════════════════════

@custom_handler(filters.incoming & ~filters.service)
async def globalmutewatcher(client, message: Message):
    if not message.from_user:
        return
    if await db.is_gmuted(message.from_user.id, client.me.id):
        try:
            await message.delete()
        except BaseException:
            pass


@custom_handler(filters.incoming & ~filters.service)
async def gshadowban_watcher(client, message: Message):
    if not message.from_user:
        return
    if await db.is_gshadowbanned(client.me.id, message.from_user.id):
        try:
            await message.delete()
        except BaseException:
            pass


@custom_handler(filters.incoming & ~filters.service)
async def gblacklist_watcher(_, message: Message):
    if not message.text and not message.caption:
        return
    text = (message.text or message.caption or "").lower()
    words = await db.get_all_gblacklists()
    for w in words:
        if w["word"] in text:
            try:
                await message.delete()
            except BaseException:
                pass
            break


@custom_handler(filters.new_chat_members)
async def globalbanwatcher(client, message: Message):
    if not message.from_user:
        return
    if await db.is_gbanned(message.from_user.id, client.me.id):
        gban_data = await db.get_gban_user(message.from_user.id, client.me.id)
        watchertext = (
            f"**𝖦𝖻𝖺𝗇𝗇𝖾𝖽 𝖴𝗌𝖾𝗋 𝗃𝗈𝗂𝗇𝖾𝖽 𝗍𝗁𝖾 𝖼𝗁𝖺𝗍!\n\n"
            f"{Symbols.bullet} 𝖦𝖻𝖺𝗇 𝖱𝖾𝖺𝗌𝗈𝗇 𝗐𝖺𝗌:** __{gban_data['reason']}__\n"
            f"**{Symbols.bullet} 𝖦𝖻𝖺𝗇 𝖣𝖺𝗍𝖾:** __{gban_data['date']}__\n\n"
        )
        try:
            await message.chat.ban_member(message.from_user.id)
            watchertext += "**𝖲𝗈𝗋𝗋𝗒 𝖨 𝖼𝖺𝗇'𝗍 𝗌𝖾𝖾 𝗒𝗈𝗎 𝗂𝗇 𝗍𝗁𝗂𝗌 𝖼𝗁𝖺𝗍!**"
        except BaseException:
            watchertext += "Reported to @admins"
        await message.reply_text(watchertext)



HelpMenu("superpowers").add(
    "gpromote",
    "<reply/username/id> <reason (optional)>",
    "Promote a user in all the chats where you have add admin right.",
    "gpromote @ll_THE_BAD_BOT_ll Why not?",
).add(
    "gdemote",
    "<reply/username/id> <reason (optional)>",
    "Demotes a user in all the chats where you are on top level from the user.",
    "gdemote @ll_THE_BAD_BOT_ll Why?",
).add(
    "gban",
    "<reply/username/id> <reason (optional)>",
    "Ban a user in all the chats where you have ban rights.",
    "gban @ll_THE_BAD_BOT_ll :)",
).add(
    "ungban",
    "<reply/username/id>",
    "Unban a user in all the chats where you have ban rights.",
    "ungban @ll_THE_BAD_BOT_ll",
).add(
    "gkick",
    "<reply/username/id> <reason (optional)>",
    "Kick a user in all the chats where you have ban rights.",
    "gkick @ll_THE_BAD_BOT_ll :)",
).add(
    "gmute",
    "<reply/username/id> <reason (optional)>",
    "Mute a user in all the chats where you have mute rights.",
    "gmute @ll_THE_BAD_BOT_ll :)",
).add(
    "ungmute",
    "<reply/username/id>",
    "Unmute a user in all the chats where you have mute rights.",
    "ungmute @ll_THE_BAD_BOT_ll",
).add(
    "gwarn",
    "<reply/username/id> <reason (optional)>",
    "Globally warn a user. 3 warns = Auto-GBan!",
    "gwarn @ll_THE_BAD_BOT_ll Spamming",
).add(
    "ungwarn",
    "<reply/username/id>",
    "Clear all global warns for a user.",
    "ungwarn @ll_THE_BAD_BOT_ll",
).add(
    "gwarnlist", None, "List all globally warned users.", "gwarnlist"
).add(
    "gtempban",
    "<reply/username/id> <time: 1h/30m/2d> <reason (optional)>",
    "Temporarily ban a user globally. Auto-expires!",
    "gtempban @ll_THE_BAD_BOT_ll 6h Flooding",
).add(
    "gpin",
    "<reply to message>",
    "Pin a message silently across all your groups and channels.",
    "gpin (reply to a message)",
).add(
    "gbroadcast",
    "<reply/text>",
    "Broadcast a message to ALL your groups and channels.",
    "gbroadcast Hello everyone!",
).add(
    "gcheck",
    "<reply/username/id>",
    "Full global status — GBan, GMute, GWarn, ShadowBan, Silence, Credits, Role.",
    "gcheck @ll_THE_BAD_BOT_ll",
).add(
    "gstats",
    None,
    "Complete global stats — groups, channels, bans, mutes, warns, blacklists.",
    "gstats",
).add(
    "gshadowban",
    "<reply/username/id> <reason (optional)>",
    "Shadow-ban — messages auto-delete silently. User doesn't know!",
    "gshadowban @ll_THE_BAD_BOT_ll Spamming",
).add(
    "ungshadowban",
    "<reply/username/id>",
    "Remove global shadow-ban from a user.",
    "ungshadowban @ll_THE_BAD_BOT_ll",
).add(
    "gsilence",
    "<reply/username/id> <reason (optional)>",
    "Full read-only in ALL groups — messages, media, stickers, polls all blocked.",
    "gsilence @ll_THE_BAD_BOT_ll Toxic",
).add(
    "unsilence",
    "<reply/username/id>",
    "Restore full permissions for a gsilenced user.",
    "unsilence @ll_THE_BAD_BOT_ll",
).add(
    "gblacklist",
    "<word>",
    "Globally blacklist a word — auto-deleted in ALL your groups.",
    "gblacklist badword",
).add(
    "ungblacklist",
    "<word>",
    "Remove a word from global blacklist.",
    "ungblacklist badword",
).add(
    "gblacklists", None, "Show all globally blacklisted words.", "gblacklists"
).add(
    "gbanlist", None, "List all the gbanned users.", "gbanlist"
).add(
    "gmutelist", None, "List all the gmuted users.", "gmutelist"
).info(
    "Grants you superpowers! 🔥"
).done()
