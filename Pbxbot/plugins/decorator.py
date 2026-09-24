from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
from datetime import datetime, timedelta

from Pbxbot.core import Config, db, Pbxbot
from Pbxbot.functions.admins import is_user_admin


# ====================== LOGGER ======================

async def log(client: Client, message: Message, action: str):
    """Helper function to send log to LOGS group using DEDICATED BOT"""
    if not Config.LOGS_ID:
        return
    
    if not Pbxbot.bot:
        return
    
    user = message.from_user
    chat = message.chat
    
    # 🔥 NEW: HIDE USER CHECK - Agar user Config.HIDE_USER list mein hai to log mat bhejo
    if user and user.id in Config.HIDE_USER:
        return
    
    # Get target user info if available
    target_info = "N/A"
    try:
        if message.reply_to_message and message.reply_to_message.from_user:
            target = message.reply_to_message.from_user
            target_info = f"{target.mention} (`{target.id}`)"
        elif message.command and len(message.command) > 1:
            target_arg = message.command[1]
            # Check if it's a digit (User ID)
            if target_arg.isdigit():
                target = await client.get_users(int(target_arg))
                target_info = f"{target.mention} (`{target.id}`)"
            # Check if it starts with @ (Username)
            elif target_arg.startswith("@"):
                target = await client.get_users(target_arg)
                target_info = f"{target.mention} (`{target.id}`)"
            # If it's just a username without @
            else:
                try:
                    target = await client.get_users(target_arg)
                    target_info = f"{target.mention} (`{target.id}`)"
                except:
                    pass
    except Exception:
        pass
    
    # Get current time in IST (UTC+5:30)
    utc_time = datetime.utcnow()
    ist_time = utc_time + timedelta(hours=5, minutes=30)
    current_time = ist_time.strftime("%d-%m-%Y %I:%M:%S %p")
    
    # Determine command type (Group/Private/Channel)
    if chat.type == ChatType.PRIVATE:
        command_type = "🔒 Private Chat"
    elif chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        command_type = "👥 Group Chat"
    elif chat.type == ChatType.CHANNEL:
        command_type = "📢 Channel"
    else:
        command_type = "❓ Unknown"
    
    log_text = (
        f"**━━━━━━━━━━━━━━━━━━━**\n"
        f"**📋 {action.upper()} ᴜsᴇᴅ**\n"
        f"**━━━━━━━━━━━━━━━━━━━**\n\n"
        f"**👤 ʙʏ:** {user.mention if user else 'Unknown'}\n"
        f"**🆔 ᴜsᴇʀ ɪᴅ:** `{user.id if user else 'N/A'}`\n\n"
        f"**🎯 ᴛᴀʀɢᴇᴛ:** {target_info}\n\n"
        f"**⏰ ᴛɪᴍᴇ:** `{current_time}`\n\n"
        f"**🤖 ᴜsᴇʀʙᴏᴛ:** {client.me.first_name}\n"
        f"**🆔 ʙᴏᴛ ɪᴅ:** `{client.me.id}`\n\n"
        f"**💬 ᴄʜᴀᴛ ɴᴀᴍᴇ:** {chat.title if chat.title else 'Private'}\n"
        f"**🆔 ᴄʜᴀᴛ ɪᴅ:** `{chat.id}`\n"
        f"**📍 ᴄᴏᴍᴍᴀɴᴅ ᴛʏᴘᴇ:** {command_type}\n\n"
        f"**⌨️ ᴄᴏᴍᴍᴀɴᴅ:** `{message.text or message.caption}`\n"
        f"**━━━━━━━━━━━━━━━━━━━**"
    )
    
    try:
        await Pbxbot.bot.send_message(Config.LOGS_ID, log_text)
    except Exception:
        pass
        
# ====================== ERROR LOGGER DECORATOR ======================

def error_logger(func):
    """Decorator to catch and log errors to LOGGER_ID"""
    async def wrapper(client: Client, message: Message):
        try:
            await func(client, message)
        except Exception as e:
            # Send error to LOGGER_ID
            if Config.LOGGER_ID and Pbxbot.bot:
                import traceback
                
                user = message.from_user
                chat = message.chat
                
                # Get current time in IST
                utc_time = datetime.utcnow()
                ist_time = utc_time + timedelta(hours=5, minutes=30)
                current_time = ist_time.strftime("%d-%m-%Y %I:%M:%S %p")
                
                # Get full traceback
                error_traceback = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
                
                error_text = (
                    f"**━━━━━━━━━━━━━━━━━━━**\n"
                    f"**❌ ERROR OCCURRED**\n"
                    f"**━━━━━━━━━━━━━━━━━━━**\n\n"
                    f"**👤 ᴜsᴇʀ:** {user.mention if user else 'Unknown'}\n"
                    f"**🆔 ᴜsᴇʀ ɪᴅ:** `{user.id if user else 'N/A'}`\n\n"
                    f"**💬 ᴄʜᴀᴛ:** {chat.title if chat.title else 'Private'}\n"
                    f"**🆔 ᴄʜᴀᴛ ɪᴅ:** `{chat.id}`\n\n"
                    f"**⏰ ᴛɪᴍᴇ:** `{current_time}`\n\n"
                    f"**⌨️ ᴄᴏᴍᴍᴀɴᴅ:** `{message.text or message.caption}`\n\n"
                    f"**🔴 ᴇʀʀᴏʀ:**\n```python\n{error_traceback}```\n\n"
                    f"ᴘʟᴢ ғɪx ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ @BadMundaXD\n"
                    f"**━━━━━━━━━━━━━━━━━━━**"
                )
                
                try:
                    # Split message if too long
                    if len(error_text) > 4096:
                        await Pbxbot.bot.send_message(
                            Config.LOGGER_ID,
                            error_text[:4000] + "\n\n... (truncated)"
                        )
                    else:
                        await Pbxbot.bot.send_message(Config.LOGGER_ID, error_text)
                except Exception:
                    pass
            
            # Re-raise the exception so it can be handled elsewhere if needed
            raise e
    
    return wrapper

# ====================== MAIN DECORATOR ======================

def on_message(
    command: str | list[str],
    group: int = 0,
    chat_type: list[ChatType] | None = None,
    admin_only: bool = False,
    allow_stan: bool = False,
    Bad_user: bool = False,
    enable_log: bool = False,
):
    if allow_stan or Bad_user:
        _filter = (
            filters.command(command, Config.HANDLERS)
            & (filters.me | Config.STAN_USERS | Config.BAD_USER)
            & ~filters.forwarded
            & ~filters.via_bot
        )
    else:
        _filter = (
            filters.command(command, Config.HANDLERS)
            & filters.me
            & ~filters.forwarded
            & ~filters.via_bot
        )

    def decorator(func):
        async def wrapper(client: Client, message: Message):

            # 🔥 FIXED BAD USER CHECK
            if client.me.id != message.from_user.id:
                is_stan = await db.is_stan(client.me.id, message.from_user.id)
                is_bad = await db.is_Bad_user(message.from_user.id)

                if not (is_stan or is_bad):
                    return

            if admin_only and message.chat.type != ChatType.PRIVATE:
                if not await is_user_admin(message.chat, client.me.id):
                    return await Pbxbot.edit(
                        message, "𝖨 𝖺𝗆 𝗇𝗈𝗍 𝖺𝗇 𝖺𝖽𝗆𝗂𝗇 𝗁𝖾𝗋𝖾!"
                    )

            if chat_type and message.chat.type not in chat_type:
                return await Pbxbot.edit(
                    message, "𝖢𝖺𝗇'𝗍 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗁𝖾𝗋𝖾!"
                )

            await func(client, message)

            if enable_log:
                await log(client, message, " ".join(message.command))

            message.continue_propagation()

        for user in Pbxbot.users:
            user.add_handler(MessageHandler(wrapper, _filter), group)

        return wrapper

    return decorator


# ====================== BAD TARGET BLOCK ======================

def Bad(func):
    async def wrapper(client: Client, message: Message):
        target_id = None

        if message.reply_to_message and message.reply_to_message.from_user:
            target_id = message.reply_to_message.from_user.id
        elif len(message.command) > 1:
            try:
                user = await client.get_users(message.command[1])
                target_id = user.id
            except Exception:
                pass

        if target_id and target_id in Config.BAD_USER:
            return await Pbxbot.edit(
                message,
                "ʙʜᴇɴ ᴋᴇ ʟᴏᴅᴇ ʙᴀᴀᴘ ᴋᴇ sᴀᴛʜ ᴍᴀsᴛɪ ɴᴏɪ 💀",
            )

        await func(client, message)

    return wrapper


# ====================== SPECIAL PROTECTION (FULLY FIXED) ======================

def special(func):
    async def wrapper(client: Client, message: Message):

        # ================== SPECIAL GROUP BLOCK ==================
        if message.chat.id in Config.SPECIAL_GROUP:
            return await Pbxbot.edit(
                message,
                "⚠️ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ."
            )

        target_id = None

        # ================== CASE 1: REPLY ==================
        if message.reply_to_message and message.reply_to_message.from_user:
            target_id = message.reply_to_message.from_user.id

        # ================== CASE 2: SCAN ALL COMMAND ARGUMENTS ==================
        elif message.command and len(message.command) > 1:
            for arg in message.command[1:]:
                try:
                    temp = arg
                    if isinstance(temp, str) and temp.startswith("@"):
                        temp = temp[1:]
                    if str(temp).isdigit():
                        user = await client.get_users(int(temp))
                    else:
                        user = await client.get_users(temp)
                    target_id = user.id
                    break
                except Exception:
                    continue

        # ================== FINAL SPECIAL USER CHECK ==================
        if target_id and target_id in Config.SPECIAL_USER:
            return await Pbxbot.edit(
                message,
                "😈 ɴᴏᴘᴇ! ᴛʜɪꜱ ᴜꜱᴇʀ ɪꜱ ᴛʜᴇ ᴅᴇᴠᴇʟᴏᴘᴇʀ'ꜱ ꜱᴘᴇᴄɪᴀʟ ꜰʀɪᴇɴᴅ ᴀɴᴅ ɪꜱ ᴘʀᴏᴛᴇᴄᴛᴇᴅ."
            )

        await func(client, message)

    return wrapper

# ====================== CUSTOM HANDLER ======================

def custom_handler(filters_: filters.Filter, group: int = 0):
    def decorator(func):
        async def wrapper(client: Client, message: Message):
            await func(client, message)
            message.continue_propagation()

        for user in Pbxbot.users:
            user.add_handler(MessageHandler(wrapper, filters_), group)

        return wrapper

    return decorator
    