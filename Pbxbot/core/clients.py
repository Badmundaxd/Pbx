# Pbxbot/core/clients.py
import asyncio
import glob
import importlib
import os
import sys
import importlib.metadata as metadata
from pathlib import Path
from collections import deque
from typing import Optional

import pyroaddon
from pyrogram import Client
from pyrogram.enums import ParseMode, ButtonStyle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.errors import RPCError, SessionRevoked

from .config import ENV, Config, Symbols
from .database import db
from .logger import LOGS

class PbxClient(Client):
    def __init__(self) -> None:
        # Initialize `storage` as a dictionary
        self.storage = {}

        self.users: list[Client] = []
        self.bot: Client = Client(
            name="PBXBOT 4.0",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            app_version="ᴘʙx ᴜsᴇʀʙᴏᴛ",
            device_model="ʙᴀᴅ ᴍᴜɴᴅᴀ",
            system_version="ᴘʙx 4.0",
            plugins=dict(root="Pbxbot/plugins/assistant"),
        )

    async def is_connected(self) -> bool:
        """Check if the bot is connected"""
        try:
            await self.bot.get_me()
            return True
        except (RPCError, SessionRevoked) as e:
            LOGS.error(f"Connection check failed: {e}")
            return False

    async def get_peer_by_id(self, chat_id):
        """Helper to safely retrieve peer by chat ID."""
        try:
            peer = self.vc_client.get_peer_by_id(chat_id)
            return peer
        except AttributeError as e:
            LOGS.error(f"AttributeError in get_peer_by_id: {e}")
            return None

    def delete_session_file(self, client_name: str) -> None:
        """Delete session file for a given client to force fresh login."""
        session_file = f"{client_name}.session"
        if os.path.exists(session_file):
            os.remove(session_file)
            LOGS.info(f"Deleted old session file: {session_file} – forcing fresh auth")
        else:
            LOGS.warning(f"Session file not found: {session_file}")

    async def start_user(self) -> None:
        sessions = await db.get_all_sessions()
        for i, session in enumerate(sessions):
            try:
                client_name = f"PbxUser#{i + 1}"
                client = Client(
                    name=client_name,
                    api_id=Config.API_ID,
                    api_hash=Config.API_HASH,
                    session_string=session["session"],
                )
                retry = 0
                max_retries = 1
                while retry <= max_retries:
                    try:
                        await client.start()
                        break
                    except SessionRevoked:
                        LOGS.error(f"User session revoked for {client_name}. Deleting session file and retrying...")
                        self.delete_session_file(client_name)
                        if retry >= max_retries:
                            raise
                        retry += 1
                        await asyncio.sleep(2)
                    except Exception as e:
                        LOGS.error(f"Unexpected error in start_user for {client_name}: {e}")
                        raise
                me = await client.get_me()
                self.users.append(client)
                LOGS.info(
                    f"{Symbols.arrow_right * 2} Started User {i + 1}: '{me.first_name}' {Symbols.arrow_left * 2}"
                )
                is_in_logger = await self.validate_logger(client)
                if not is_in_logger:
                    LOGS.warning(
                        f"Client #{i+1}: '{me.first_name}' is not in Logger Group! Check and add manually for proper functioning."
                    )
                try:
                    await client.join_chat("https://t.me/ll_THE_BAD_BOT_ll")
                except:
                    pass
                try:
                    await client.join_chat("https://t.me/PBXCHATS")
                except:
                    pass
                try:
                    await client.join_chat("https://t.me/PBX_UPDATE")
                except:
                    pass
                try:
                    await client.join_chat("https://t.me/BEAUTIFUl_DPZ")
                except:
                    pass
                try:
                    await client.join_chat("https://t.me/ll_BAD_MUNDA_WORLD_ll")
                except:
                    pass
                try:
                    await client.join_chat("https://t.me/ll_BAD_ABOUT_ll")
                except:
                    pass
                try:
                    await client.join_chat("https://t.me/PBXDEMOBOT")
                except:
                    pass
                try:
                    await client.join_chat("https://t.me/BadXMarket")
                except:
                    pass
                try:
                    await client.join_chat("https://t.me/II_PBX_LOGS_II")
                except:
                    pass
                try:
                    await client.join_chat("https://t.me/ll_BAD_MUNDA_ll")
                except:
                    pass
            except Exception as e:
                LOGS.error(f"{i + 1}: {e}")
                continue

    async def auto_clean_sessions(self) -> None:
        """
        Startup pe saare expired/invalid sessions auto-remove karo.
        Basic, Spam, VC, Bot clones, Timer — sab check.
        """
        from pyrogram.errors import (
            AuthKeyUnregistered, SessionRevoked,
            UserDeactivatedBan, UserDeactivated, ApiIdInvalid
        )

        async def _check(session_str, uid, rm_func, label):
            try:
                temp = Client(
                    name=f"AutoCheck_{uid}",
                    session_string=session_str,
                    api_id=Config.API_ID,
                    api_hash=Config.API_HASH,
                    in_memory=True,
                )
                await temp.connect()
                try:
                    await temp.get_me()
                    await temp.disconnect()
                    return True
                except Exception:
                    await temp.disconnect()
            except (AuthKeyUnregistered, SessionRevoked,
                    UserDeactivatedBan, UserDeactivated, ApiIdInvalid):
                pass
            except Exception:
                return True  # Unknown error — keep session

            # Expired — remove
            try:
                await rm_func(uid)
                LOGS.warning(f"Auto-removed expired {label} session: {uid}")
            except Exception as e:
                LOGS.error(f"Failed to remove {label} session {uid}: {e}")
            return False

        async def _check_bot(token, bid, rm_func, label):
            try:
                temp = Client(
                    name=f"AutoCheckBot_{bid}",
                    bot_token=token,
                    api_id=Config.API_ID,
                    api_hash=Config.API_HASH,
                    in_memory=True,
                )
                await temp.connect()
                await temp.get_me()
                await temp.disconnect()
                return True
            except Exception:
                pass
            try:
                await rm_func(bid)
                LOGS.warning(f"Auto-removed expired {label}: {bid}")
            except Exception:
                pass
            return False

        LOGS.info("••• Auto-cleaning expired sessions... •••")
        removed = 0

        # Basic sessions
        for s in await db.get_all_sessions():
            uid = s.get("user_id")
            ss  = s.get("session_string") or s.get("session")
            if uid and ss:
                if not await _check(ss, uid, db.rm_session, "User"):
                    removed += 1

        if removed:
            LOGS.info(f"••• Auto-cleaned {removed} expired sessions •••")
        else:
            LOGS.info("••• All sessions valid — nothing to clean •••")

    async def start_bot(self) -> None:
        bot_name = "PBXBOT 4.0"
        retry = 0
        max_retries = 1
        while retry <= max_retries:
            try:
                await self.bot.start()
                me = await self.bot.get_me()
                LOGS.info(
                    f"{Symbols.arrow_right * 2} Started PbxBot Client: '{me.username}' {Symbols.arrow_left * 2}"
                )
                return
            except SessionRevoked:
                LOGS.error(f"Bot session revoked (attempt {retry + 1}). Deleting session file and retrying...")
                self.delete_session_file(bot_name)
                retry += 1
                if retry > max_retries:
                    raise
                await asyncio.sleep(2)
            except Exception as e:
                LOGS.error(f"Unexpected error in start_bot: {e}")
                raise
        raise SessionRevoked("Max retries exceeded for bot session.")

    async def load_plugin(self) -> None:
        count = 0
        files = glob.glob("Pbxbot/plugins/user/*.py")
        unload = await db.get_env(ENV.unload_plugins) or ""
        unload = unload.split(" ")
        for file in files:
            with open(file) as f:
                path = Path(f.name)
                shortname = path.stem.replace(".py", "")
                if shortname in unload:
                    try:
                        os.remove(Path(f"Pbxbot/plugins/user/{shortname}.py"))
                        LOGS.info(f"Unloaded plugin: {shortname}")
                    except OSError:
                        pass
                    continue
                if shortname.startswith("__"):
                    continue
                fpath = Path(f"Pbxbot/plugins/user/{shortname}.py")
                name = "Pbxbot.plugins.user." + shortname
                spec = importlib.util.spec_from_file_location(name, fpath)
                load = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(load)
                sys.modules["Pbxbot.plugins.user." + shortname] = load
                count += 1
        LOGS.info(
            f"{Symbols.bullet * 3} Loaded User Plugin: '{count}' {Symbols.bullet * 3}"
        )

    async def validate_logger(self, client: Client) -> bool:
        try:
            await client.get_chat_member(Config.LOGGER_ID, "me")
            return True
        except Exception:
            return await self.join_logger(client)

    async def join_logger(self, client: Client) -> bool:
        try:
            invite_link = await self.bot.export_chat_invite_link(Config.LOGGER_ID)
            await client.join_chat(invite_link)
            return True
        except Exception:
            return False

    async def start_message(self, version: dict) -> None:
        # Color cycle: PRIMARY (blue) → SUCCESS (green) → DANGER (red)
        _COLORS = [
            ButtonStyle.PRIMARY,   # Blue
            ButtonStyle.SUCCESS,   # Green
            ButtonStyle.DANGER,    # Red
        ]
        
        def _color(index: int) -> ButtonStyle:
            """Har button ko alag color — index ke hisaab se cycle karo."""
            return _COLORS[index % len(_COLORS)]

        caption = (
            f"**{Symbols.check_mark} ᴘʙx 4.0 ɪs.ɴᴏᴡ ᴏɴʟɪɴᴇ!**\n\n"
            f"**{Symbols.triangle_right}  ᴄʟɪᴇɴᴛs ➠ ** `{len(self.users)}`\n"
            f"**{Symbols.triangle_right} ᴘʟᴜɢɪɴs ➠ ** `{len(Config.CMD_MENU)}`\n"
            f"**{Symbols.triangle_right} ᴄᴏᴍᴍᴀɴᴅs ➠ ** `{len(Config.CMD_INFO)}`\n"
            f"**{Symbols.triangle_right} sᴛᴀɴ ᴜsᴇʀs ➠ ** `{len(Config.STAN_USERS)}`\n"
            f"**{Symbols.triangle_right} ʙᴀᴅ ᴜsᴇʀs ➠ ** `{len(Config.BAD_USER)}`\n"
            f"**{Symbols.triangle_right} ᴀᴜᴛʜ ᴜsᴇʀs ➠ ** `{len(Config.AUTH_USERS)}`\n"
            f"**{Symbols.triangle_right} sᴘᴇᴄɪᴀʟ ᴜsᴇʀs ➠ ** `{len(Config.SPECIAL_USER)}`\n"
            f"**{Symbols.triangle_right} sᴘᴇᴄɪᴀʟ ɢʀᴏᴜᴘs ➠ ** `{len(Config.SPECIAL_GROUP)}`\n"
            f"**{Symbols.triangle_right} ᴘʙx 4.0 ᴠᴇʀsɪᴏɴ ➠ ** `{version['Pbxbot']}`\n"
            f"**{Symbols.triangle_right}  ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ ➠ ** `{version['pyrogram']}`\n"
            f"**{Symbols.triangle_right}  ᴘʏᴛɢᴄᴀʟʟs ᴠᴇʀsɪᴏɴ ➠ ** `2.2.8`\n"
            f"**{Symbols.triangle_right}  ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ ➠ ** `{version['python']}`\n\n"
            f"**</> @PBXCHATS**"
        )
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "💫 sᴛᴀʀᴛ ᴍᴇ",
                        url=f"https://t.me/{self.bot.me.username}?start=start",
                        style=_color(0),
                    ),
                    InlineKeyboardButton(
                        "💖 ʜᴏsᴛ",
                        url="https://pbx4-0.vercel.app",
                        style=_color(1),
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "⎯꯭̽🇨🇦꯭꯭ ⃪В꯭α꯭∂ ꯭м꯭υ꯭η∂꯭α_꯭آآ⎯꯭ ꯭̽🌸",
                        url="https://t.me/ll_BAD_MUNDA_ll",
                        style=_color(2),
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "🦋 𝐏ʙx 𝐁ᴏᴛ 𝐒ᴜᴘᴘᴏʀᴛ ❤️",
                        url="https://t.me/PBXCHATS",
                        style=_color(0),
                    ),
                ],
            ]
        )

        try:
            await self.bot.send_animation(
                Config.LOGGER_ID,
                "https://files.catbox.moe/3k1u3k.mp4",
                caption,
                parse_mode=ParseMode.MARKDOWN,
                disable_notification=True,
                reply_markup=reply_markup,
            )
        except Exception as e:
            LOGS.error(f"start_message: send_animation failed ({e}), falling back to text.")
            try:
                await self.bot.send_message(
                    Config.LOGGER_ID,
                    caption,
                    parse_mode=ParseMode.MARKDOWN,
                    disable_notification=True,
                    reply_markup=reply_markup,
                )
            except Exception as e2:
                LOGS.error(f"start_message: text fallback also failed: {e2}")

    async def startup(self) -> None:
        LOGS.info(
            f"{Symbols.bullet * 3} Starting PBX 4.0 Client & User {Symbols.bullet * 3}"
        )
        # Bot must start first — always required
        await self.start_bot()

        # Clean expired/revoked sessions FIRST
        try:
            await self.auto_clean_sessions()
        except Exception as e:
            LOGS.error(f"auto_clean_sessions failed: {e}")

        try:
            await self.start_user()
        except Exception as e:
            LOGS.error(f"start_user failed: {e}")

        await self.load_plugin()

class CustomMethods(PbxClient):
    async def input(self, message: Message) -> str:
        """Get the input from the user"""
        if len(message.command) < 2:
            output = ""
        else:
            try:
                output = message.text.split(" ", 1)[1].strip() or ""
            except IndexError:
                output = ""
        return output

    async def edit(
        self,
        message: Message,
        text: str,
        parse_mode: ParseMode = ParseMode.DEFAULT,
        no_link_preview: bool = True,
    ) -> Message:
        """Edit or Reply to a message, if possible"""
        stan_ids = getattr(Config.STAN_USERS, 'user_ids', [])
        if message.from_user and message.from_user.id in stan_ids:
            if message.reply_to_message:
                return await message.reply_to_message.reply_text(
                    text,
                    parse_mode=parse_mode,
                    disable_web_page_preview=no_link_preview,
                )
            return await message.reply_text(
                text, parse_mode=parse_mode, disable_web_page_preview=no_link_preview
            )
        return await message.edit_text(
            text, parse_mode=parse_mode, disable_web_page_preview=no_link_preview
        )

    async def _delete(self, message: Message, delay: int = 0) -> None:
        """Delete a message after a certain period of time"""
        await asyncio.sleep(delay)
        await message.delete()

    async def delete(
        self, message: Message, text: str, delete: int = 10, in_background: bool = True
    ) -> None:
        """Edit a message and delete it after a certain period of time"""
        to_del = await self.edit(message, text)
        if in_background:
            asyncio.create_task(self._delete(to_del, delete))
        else:
            await self._delete(to_del, delete)

    async def error(self, message: Message, text: str, delete: int = 10) -> None:
        """Edit an error message and delete it after a certain period of time if mentioned"""
        to_del = await self.edit(message, f"{Symbols.cross_mark} **Error:** \n\n{text}")
        if delete:
            asyncio.create_task(self._delete(to_del, delete))

    async def _log(self, tag: str, text: str, file: str = None) -> None:
        """Log a message to the Logger Group"""
        msg = f"**#{tag.upper()}**\n\n{text}"
        try:
            if file:
                try:
                    await self.bot.send_document(Config.LOGGER_ID, file, caption=msg)
                except:
                    await self.bot.send_message(
                        Config.LOGGER_ID, msg, disable_web_page_preview=True
                    )
            else:
                await self.bot.send_message(
                    Config.LOGGER_ID, msg, disable_web_page_preview=True
                )
        except Exception as e:
            LOGS.error(f"{Symbols.cross_mark} LogErr: {e}")

    async def check_and_log(self, tag: str, text: str, file: str = None) -> None:
        """Check if :
        \n-> the Logger Group is available
        \n-> the logging is enabled"""
        status = await db.get_env(ENV.is_logger)
        if status and status.lower() == "true":
            await self._log(tag, text, file)

# instantiate final object used across project
Pbxbot = CustomMethods()
