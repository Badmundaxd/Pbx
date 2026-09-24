import random
import asyncio

from pyrogram import Client, filters
from pyrogram.enums import ChatAction as CA
from pyrogram.types import Message

from . import *

RAID_STR = [
   "🥹ਬਾਰੀ ਬਰਸੀ ਖੱਟਣ ਗਿਆ ਸੀ ਖੱਟ ਕੇ ਲਿਆਂਦਾ ਬੱਲਾ ਤੇਰੀ ਭੈਣ ਦਾ ਫੁੱਦਾ ਮਾਰੇ ਗਰੁੱਪ ਦਾ ਮੇਂਬਰ ਕੱਲਾ ਕੱਲਾ😭",
"😈ਬਾਰੀ ਬਰਸੀ ਖੱਟਣ ਗਿਆ ਸੀ ਖੱਟ ਕੇ ਲਿਆਂਦਾ ਆਲੂ ਪਿਓ ਤੇਰਾ ਟੈਮਪੂ ਮਾਂ ਤੇਰੀ ਚਾਲੂ😈",
"🥵ਬਾਰੀ ਬਰਸੀ ਖੱਟਣ ਗਿਆ ਸੀ ਖੱਟ ਕੇ ਲਿਆਂਦਾ ਫੂਸਾ ਮੇਰਾ ਡੈਡੀ ਤੇਰੀ ਬੁੰਡ ਮਾਰੇ ਮੈ ਮਾਰਾਂ ਤੇਰੀ ਭੈਣ ਦਾ ਘੁਸਾ👅",
"🥵ਵਾਰੀ ਵਰਸੀ ਖੱਟਣ ਗਿਆ ਸੀ ਖੱਟ ਕੇ ਲਿਆਂਦਾ ਸ਼ੇਮਪੂ ਮਾਂ ਤੇ bhen ਤੇਰੀ ਸਿੱਰੇ ਦੀ ਟੈਕਸੀ ਤੂੰ ਤੇ ਤੇਰਾ ਪਿਓ ਪਿੰਡ ਦੇ ਮਸ਼ਹੂਰ ਟੈਮਪੂ👅",
"😈ਵਾਰੀ ਵਰਸੀ ਖੱਟਣ ਗਿਆ ਸੀ ਖੱਟ ਕੇ ਲਿਆਂਦਾ ਵੱਟਾ ਮਾਂ ਤੇ ਤੇਰੀ ਭੈਣ ਦੇ ਲੁੱਲਾ ਪਾਵਾ ਤੇਰਾ ਪਿਓ ਥੱਲੋ ਦੀ ਚੁੰਗੇ ਮੇਰਾ ਟੱਟਆ👅",
"🥺ਵਾਰੀ ਵਰਸੀ ਖੱਟਣ ਗਿਆ ਸੀ ਖੱਟ ਕੇ ਲਿਆਂਦਾ ਅੰਬਾ ਤੇਰੀ ਮਾਂ ਦੇ ਸ਼ੋਲ਼ੇ ਚ ਮਾਰਾਂ 90 ਗਜ ਦਾ ਟੰਬਾ😭",
"🥹ਬਾਰੀ ਬਰਸੀ ਖੱਟਣ ਗਿਆ ਸੀ ਖੱਟ ਕੇ ਲਿਆਂਦਾ ਟੰਬਾ ਤੇਰੀ ਮਾਂ ਤੇ ਚੜਜੇ ਮੇਰਾ ਪਿਓ ਤੇ me ਤੇਰੀ ਬੁੰਡ ਚ ਮਾਰਾਂ ਖਮਬਾ😈",
"😭ਬਾਰੀ ਬਰਸੀ ਖੱਟਣ ਗਿਆ ਸੀ ਖੱਟ ਕੇ ਲਿਆਂਦਾ ਫੇਬੂ ਤੇਰੀ ਮਾਂ ਦਾ ਫੁੱਦੜਾ ਮਾਰੇ ਸਾਡੇ ਪਿੰਡ ਵਾਲਾ ਬਿੱਕਰ ਸੇਬੂ🥵",
"👅ਬੜੀ ਬਰਸੀ ਖੱਟਣ ਗਿਆ ਸੀ ਖੱਟ ਕੇ ਲਿਆਂਦੀ ਲਾਲੀ ਤੇਰੇ ਪਿਓ ਦੇ ਮਾਰਾਂ ਲੁੱਲਾ ਤੇਰੀ ਭੈਣ ਦੇ ਸ਼ੋਲ਼ੇ ਚ ਟਰਾਲ਼ੀ👅",
"🥵ਬਾਰੀ ਬਰਸੀ ਖੱਟਣ ਗਏ ਸੀ ਖੱਟ ਕੇ ਲਿਆਂਦਾ ਬੈਡ ਤੇਰੀ ਮਾਂ ਤੇ ਤੇਰੇ ਪਿਓ ਦੀ ਪੱਟਾਂ ਬੁੰਡ ਤੇਰੀ ਭੈਣ ਦੇ ਫੁੜਦੇ ਚ ਸ਼ੈੱਡ😭",
"🥹ਬਾਰੀ ਬਰਸੀ ਖੱਟਣ ਗਿਆ ਸੀ ਖੱਟ ਕੇ ਲਿਆਂਦੀ ਰੀਡ ਆਵਦੀ ਮਾਂ ਤੇ ਭਵਨ ਕਰ ਨੰਗੀ ਜੇ ਮੈਚ ਨੀ ਹੁੰਦੀ ਸਪੀਡ🥹",
"🥵ਕਹਿੰਦੇ ਆਰ ਟਾਂਗਾ ਪਾਰ ਟਾਂਗਾ ਵਿਚ ਟਾਂਗਾ ਦੇ ਟੋਏ ਤੇਰੀ ਭੈਣ ਦਾ ਫੁੱਦਾ ਮਾਰਾਂ ਤੇਰਾ ਪਿਓ ਕੋਲ ਖੜਾ ਕਰੇ ਓਏ ਓਏ🥹"
"👅ਕਹਿੰਦੇ ਆਰ ਟਾਂਗਾ ਪਾਰ ਟਾਂਗਾ ਵਿਚ ਟਾਂਗਾ ਦੇ ਹੁਲ ਤੇਰੀ ਮਾਂ ਦੀ ਮਾਰਾਂ ਸ਼ੋਲੀ ਤੇਰੀ ਭੈਣ ਦੇ ਫੁੜਦੇ ਚ 10 ਗਜ ਦਾ ਲੁੱਲ🥵",
"😭ਬਾਰੀ ਬਰਸੀ ਖੱਟਣ ਗਿਆ ਸੀ ਖੱਟ ਕੇ ਲਿਆਂਦੀ ਤੋਰੀ ਪਿਓ ਤੇਰਾ ਸ਼ੱਕਾ ਤੇਰੀ ਮਾਂ ਦੀ ਫੁੱਦੀ ਚ ਬਹੁਤ ਵੱਡੀ ਮੋਰੀ😭",
"🥵ਬਾਰੀ ਬਰਸੀ ਖੱਟਣ ਗਿਆ ਸੀ ਖੱਟ ਕੇ ਲਿਆਂਦਾ ਕੱਮ ਤੇਰਾ ਪਿਓ ਲਾਵੇ ਚੁੱਪੇ ਤੇਰੀ ਭੈਣ ਦੇ ਫੁੜਦੇ ਚ ਡਰੱਮ👅",
"ਕੱਚ ਦੀ ਗਲਾਸੀ ਵਿਚ ਬੂਟਾ ਭੰਗ ਦਾ ਇੱਕ ਵਾਰ ਦੇਦੇ ਫੇਰ ਨੀ ਮੰਗਦਾ",
"ਕੱਚ ਦੇ ਗਲਸ ਵਿਚ 🥵👅 ਤੋਤਾ ਬੋਲਦਾ 🥵👅ਤੇਰੇ ਵਰਗੇ ਦੀ ਮੈ ਤੁਰੇ ਜਾਂਦੇ 🥵👅",
"ਵਾਰ ੀ ਵਰਸੀ ਖੱਟਣ ਗਿਆ ਸੀ 🥵👅 ਖੱਟ ਕੇ ਲਿਆਂਦਾ ਪੋਲਾ 🥵👅 ਤੇਰੀ ਭੈਣ ਦੀ ਫੁੱਦੀ 🥵👅 ਤੇਰੀ ਮਾਂ ਦਾ ਪਾਟਿਆ ਸ਼ੋਲਾ 🥵👅",
"ਜੱਟ ਬੈਠਾ ਛਾਵੇ ਤੂਤ ਤੇਰੀ ਭੈਣ ਦੀ ਭੋਸੜੀ ਵਿਚ ਦੇਵਾ ਮੂਤ ",
"ਜੱਟ ਕਰਦਾ ਹੁਣ ਕੰਮ੍ਰ  ਜਾ ਸਾਲਿਆ ਆਪਣੀ ਭੈਣ ਦੀ ਭੋਸੜੀ ਦਾ ਨਾਲਾ ਜਾ ਕੇ ਬੰਨ",
"ਜੱਟ ਖੜਾ ਕੋਲ ਨਹਿਰ ਏ  ਪਹਿਲੇ ਪਹਿਰ ਚੜਿਆ ਤੇਰੀ ਭੈਣ ਤੇ ਉੱਤਰਿਆ ਚੌਥੇ ਪਹਿਰ ਏ",
"ਜੱਟ ਦੀ ਪੂਰੀ ਸਿਰੇ ਦੀ ਟੀਮ  ਤੇਰੀ ਬੁੰਡ ਚ ਪਾਉਣਾ ਸੱਤ ਫੁੱਟ ਸਰਿਆ ਦਾ ਵੀਮ",  
"ਕੇਹਂਦਾ ਬਾਰੀ ਬਰਸੀ ਖਟਨ ਗਿਆ ਖਟ ਕੇ ਲਿਆਂਦਾ ਕਲਿਪ ਫੁਦੀ ਵਿਚ ਲਨ ਵੜ ਗਿਆ ਟਟੇ ਮਾਰਨ ਸਲਿਪ",
"ਕੇਹਂਦਾ ਬਾਰੀ ਬਰਸੀ ਖਟਨ ਗਯਾ ਸੀ ਖੱਟ ਕੇ ਲਿਆਂਦੀ ਸ਼ੇਨੀ ਮੇਰੀ ਭਾਵੇਂ ਲਤ ਟੁੱਟ ਜਾਏ ਪਰਤੇਰੀ ਮੰਮੀ  ਦੀ ਫੁਦੀ ਕੰਦ ਓਥੇ ਭਠਾ ਕੇ ਲੈਣੀ 👅👅",
"ਕਹਿੰਦੇ ਤਾਰਾ ਤਾਰਾ ਤੇਰੀ ਭੇਣ ਦੀ ਚਕ ਕੇ ਲਤ ਬੁੰਡ ਮਾਰਾ👅👅👅",
"ਕੇਹਂਦਾ ਗਹਾਰਾ  ਗਹਾਰਾ ਮੁੜਕੇ ਤੂੰ ਇਹ ਗਰੁੱਪ ਚ ਨਹੁ ਦਿਖਣਾ ਜਦੋਂ ਲਨ ਚਕ ਤਾਂ ਤੇਰੇ  ਸਾਰਾ",
]

COLLECTION_NAME = "punjabi_raid_targets"

async def get_raid_targets(bot_id):
    data = await db.get_doc(COLLECTION_NAME, bot_id)
    if not data:
        await db.set_doc(COLLECTION_NAME, bot_id, {"targets": []})
        return []
    return data.get("targets", [])

async def add_raid_target(bot_id, user_id):
    targets = await get_raid_targets(bot_id)
    if user_id not in targets:
        targets.append(user_id)
        await db.update_doc(COLLECTION_NAME, bot_id, {"targets": targets})

async def remove_raid_target(bot_id, user_id):
    targets = await get_raid_targets(bot_id)
    if user_id in targets:
        targets.remove(user_id)
        await db.update_doc(COLLECTION_NAME, bot_id, {"targets": targets})

async def is_raid_active(bot_id, user_id):
    targets = await get_raid_targets(bot_id)
    return user_id in targets

@custom_handler(filters.all & ~filters.private, group=-15)
async def punjabi_reply_raid_handler(c: Client, m: Message):
    if not m.from_user:
        return
    bot_id = c.me.id
    user_id = m.from_user.id
    if not await is_raid_active(bot_id, user_id):
        return
    message = random.choice(RAID_STR)
    await c.send_chat_action(m.chat.id, CA.TYPING)
    await asyncio.sleep(1)
    await m.reply_text(message)
    await c.send_chat_action(m.chat.id, CA.CANCEL)
    
    
@on_message("preplyraid", allow_stan=True)
async def activate_preplyraid(c: Client, m: Message):
    bot_id = c.me.id

    if m.reply_to_message and m.reply_to_message.from_user:
        target_user = m.reply_to_message.from_user
    else:
        try:
            target = m.command[1]
            if m.entities and len(m.entities) > 1 and m.entities[1].type == "text_mention":
                target_user = m.entities[1].user
            else:
                target_user = await c.get_users(target)
        except:
            return await Pbxbot.delete(m, "`Reply to a user or provide username/ID.`")

    if target_user.is_self or target_user.id in Config.DEVS:
        return await Pbxbot.delete(m, "`Can't raid myself or devs.`")

    username = f"@{target_user.username}" if target_user.username else target_user.mention
    msg = await m.reply_text("`Activating Punjabi Reply Raid...`")

    if await is_raid_active(bot_id, target_user.id):
        return await msg.edit(f"`Punjabi raid already active on {username}`")

    await add_raid_target(bot_id, target_user.id)
    await msg.edit(f"**✅ Punjabi Reply Raid Activated on {username}**")


@on_message("dpreplyraid", allow_stan=True)
async def deactivate_preplyraid(c: Client, m: Message):
    bot_id = c.me.id

    if m.reply_to_message and m.reply_to_message.from_user:
        target_user = m.reply_to_message.from_user
    else:
        try:
            target = m.command[1]
            if m.entities and len(m.entities) > 1 and m.entities[1].type == "text_mention":
                target_user = m.entities[1].user
            else:
                target_user = await c.get_users(target)
        except:
            return await Pbxbot.delete(m, "`Reply to a user or provide username/ID.`")

    username = f"@{target_user.username}" if target_user.username else target_user.mention
    msg = await m.reply_text("`Deactivating Punjabi Reply Raid...`")

    if not await is_raid_active(bot_id, target_user.id):
        return await msg.edit(f"`No active Punjabi raid on {username}`")

    await remove_raid_target(bot_id, target_user.id)
    await msg.edit(f"**❌ Punjabi Reply Raid Deactivated on {username}**")


HelpMenu("preplyraid").add(
    "preplyraid", "<reply/username/id>", "Start Punjabi reply raid (only this session).", "preplyraid @username"
).add(
    "dpreplyraid", "<reply/username/id>", "Stop Punjabi reply raid.", "dpreplyraid @username"
).info(
    "Punjabi Reply Raid Module\n- Independent per session\n- May cause floodwaits!"
).done()
