import os

from pyrogram import Client
from pyrogram.raw.functions.users import GetFullUser
from pyrogram.types import Message

from . import HelpMenu, db, Pbxbot, on_message, Bad, special


# ─────────────────────────────────────────────
#  .clone — copy full profile of replied user
# ─────────────────────────────────────────────
@on_message("clone", allow_stan=True, Bad_user=True)
@Bad
@special
async def clone(client: Client, message: Message):
    if not message.reply_to_message:
        return await Pbxbot.delete(
            message, "Reply to a user's message to clone their profile."
        )

    replied_user = message.reply_to_message.from_user
    if replied_user.is_self:
        return await Pbxbot.delete(message, "I can't clone myself!")

    Pbx = await Pbxbot.edit(message, "Cloning ...")

    # Save current profile so we can revert later
    try:
        meh = await client.resolve_peer(client.me.id)
        fullUser = await client.invoke(GetFullUser(id=meh))
        about = fullUser.full_user.about or ""
    except Exception:
        about = ""

    await db.set_env("CLONE_FIRST_NAME", client.me.first_name)
    await db.set_env("CLONE_LAST_NAME", client.me.last_name or "")
    await db.set_env("CLONE_ABOUT", about)

    # Apply target user's profile
    try:
        targetUser = await client.resolve_peer(replied_user.id)
        repliedFullUser = await client.invoke(GetFullUser(id=targetUser))
        await client.update_profile(
            first_name=replied_user.first_name,
            last_name=replied_user.last_name or "",
            about=repliedFullUser.full_user.about or "",
        )
    except Exception:
        await client.update_profile(
            first_name=replied_user.first_name,
            last_name=replied_user.last_name or "",
        )

    try:
        profile_pic = await client.download_media(replied_user.photo.big_file_id)
        await client.set_profile_photo(photo=profile_pic)
        os.remove(profile_pic)
    except Exception:
        pass

    await Pbx.edit("**Cloned successfully!**")
    await Pbxbot.check_and_log(
        "clone",
        f"**Cloned {replied_user.mention}** ({replied_user.id})\n\n**By:** {client.me.first_name}",
    )


# ─────────────────────────────────────────────
#  .revert — restore original profile
# ─────────────────────────────────────────────
@on_message("revert", allow_stan=True, Bad_user=True)
async def revert(client: Client, message: Message):
    first_name = await db.get_env("CLONE_FIRST_NAME")
    last_name = await db.get_env("CLONE_LAST_NAME")
    about = await db.get_env("CLONE_ABOUT")

    if not first_name:
        return await Pbxbot.delete(message, "Nothing to revert — you haven't cloned anyone.")

    Pbx = await Pbxbot.edit(message, "Reverting ...")

    await client.update_profile(first_name, last_name, about)

    async for photos in client.get_chat_photos("me", 1):
        await client.delete_profile_photos(photos.file_id)

    await db.rm_env("CLONE_FIRST_NAME")
    await db.rm_env("CLONE_LAST_NAME")
    await db.rm_env("CLONE_ABOUT")

    await Pbx.edit("**Reverted back to original profile!**")
    await Pbxbot.check_and_log(
        "revert",
        f"**Reverted to original profile.**\n\n**By:** {first_name}",
    )


# ─────────────────────────────────────────────
#  .setname — change only first/last name
#  Usage: .setname John Doe  or  .setname John
# ─────────────────────────────────────────────
@on_message("setname", allow_stan=True, Bad_user=True)
async def setname(client: Client, message: Message):
    if len(message.command) < 2:
        return await Pbxbot.delete(message, "Usage: `.setname FirstName LastName`")

    parts = message.command[1:]
    first_name = parts[0]
    last_name = " ".join(parts[1:]) if len(parts) > 1 else ""

    Pbx = await Pbxbot.edit(message, "Updating name ...")
    await client.update_profile(first_name=first_name, last_name=last_name)
    await Pbx.edit(f"**Name updated!**\n`{first_name} {last_name}`.strip()")


# ─────────────────────────────────────────────
#  .setbio — change only bio/about
#  Usage: .setbio Your new bio here
# ─────────────────────────────────────────────
@on_message("setbio", allow_stan=True, Bad_user=True)
async def setbio(client: Client, message: Message):
    if len(message.command) < 2:
        return await Pbxbot.delete(message, "Usage: `.setbio Your bio text here`")

    bio = " ".join(message.command[1:])
    if len(bio) > 70:
        return await Pbxbot.delete(message, "Bio cannot exceed 70 characters!")

    Pbx = await Pbxbot.edit(message, "Updating bio ...")
    await client.update_profile(bio=bio)
    await Pbx.edit(f"**Bio updated!**\n`{bio}`")


# ─────────────────────────────────────────────
#  .setdp — change only profile photo
#  Usage: reply to a photo with .setdp
# ─────────────────────────────────────────────
@on_message("setdp", allow_stan=True, Bad_user=True)
async def setdp(client: Client, message: Message):
    reply = message.reply_to_message

    if not reply or not reply.photo:
        return await Pbxbot.delete(message, "Reply to a photo to set it as your profile picture!")

    Pbx = await Pbxbot.edit(message, "Updating profile photo ...")

    try:
        photo_path = await client.download_media(reply.photo.file_id)
        await client.set_profile_photo(photo=photo_path)
        os.remove(photo_path)
        await Pbx.edit("**Profile photo updated!**")
    except Exception as e:
        await Pbx.edit(f"❌ Failed to update photo: `{e}`")


# ─────────────────────────────────────────────
#  HELP MENU
# ─────────────────────────────────────────────
HelpMenu("clone").add(
    "clone",
    "<reply to user's message>",
    "Clone the full profile of the replied user (name, bio & photo).",
    "clone",
    "Only the last profile is saved for revert. Clone with caution!",
).add(
    "revert",
    None,
    "Revert back to your original profile before cloning.",
    "revert",
).add(
    "setname",
    "<firstname> [lastname]",
    "Change only your display name without affecting bio or photo.",
    "setname John Doe",
).add(
    "setbio",
    "<text>",
    "Change only your bio/about text. Max 70 characters.",
    "setbio Just chilling 🎧",
).add(
    "setdp",
    "<reply to photo>",
    "Change only your profile photo by replying to any image.",
    "setdp",
).info(
    "Clone & Profile Menu"
).done()
