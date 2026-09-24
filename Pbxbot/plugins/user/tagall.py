from . import *
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import UserNotParticipant
from pyrogram.types import ChatPermissions

spam_chats = []

EMOJI = [ "🦋🦋🦋🦋🦋",
          "🧚🌸🧋🍬🫖",
          "🥀🌷🌹🌺💐",
          "🌸🌿💮🌱🌵",
          "❤️💚💙💜🖤",
          "💓💕💞💗💖",
          "🌸💐🌺🌹🦋",
          "🍔🦪🍛🍲🥗",
          "🍎🍓🍒🍑🌶️",
          "🧋🥤🧋🥛🍷",
          "🍬🍭🧁🎂🍡",
          "🍨🧉🍺☕🍻",
          "🥪🥧🍦🍥🍚",
          "🫖☕🍹🍷🥛",
          "☕🧃🍩🍦🍙",
          "🍁🌾💮🍂🌿",
          "🌨️🌥️⛈️🌩️🌧️",
          "🌷🏵️🌸🌺💐",
          "💮🌼🌻🍀🍁",
          "🧟🦸🦹🧙👸",
          "🧅🍠🥕🌽🥦",
          "🐷🐹🐭🐨🐻‍❄️",
          "🦋🐇🐀🐈🐈‍⬛",
          "🌼🌳🌲🌴🌵",
          "🥩🍋🍐🍈🍇",
          "🍴🍽️🔪🍶🥃",
          "🕌🏰🏩⛩️🏩",
          "🎉🎊🎈🎂🎀",
          "🪴🌵🌴🌳🌲",
          "🎄🎋🎍🎑🎎",
          "🦅🦜🕊️🦤🦢",
          "🦤🦩🦚🦃🦆",
          "🐬🦭🦈🐋🐳",
          "🐔🐟🐠🐡🦐",
          "🦩🦀🦑🐙🦪",
          "🐦🦂🕷️🕸️🐚",
          "🥪🍰🥧🍨🍨",
          " 🥬🍉🧁🧇",
        ]

GM_TAG = [ "**ਗੁੱਡ ਮੋਰਨਿੰਗ 💘🌷**",
"ਗੁੱਡ ਮੋਰਨਿੰਗ 👀🕊️**",
"ਗੁੱਡ ਮੋਰਨਿੰਗ 🌾💸**",
"ਗੁੱਡ ਮੋਰਨਿੰਗ ☕🍩**",
"ਗੁੱਡ ਮੋਰਨਿੰਗ 👀🇺🇲**",
"ਗੁੱਡ ਮੋਰਨਿੰਗ 🍼😚**",
"ਗੁੱਡ ਮੋਰਨਿੰਗ 😍😘**",
"ਗੁੱਡ ਮੋਰਨਿੰਗ ਮੇਰੀ ਜਾਣ👀😚**",
"ਹਾਂਜੀ ਗੁੱਡ ਮੋਰਨਿੰਗ ਸੋਣਯੋ 🫶🏻😍**",
"ਉਠੋ ਜੀ 😿💘**",
"ਤੁਸੀ ਉਠੇ ਨਹੀਂ ਹਲੇ 😿😍**",        
]


GN_TAG = [ "**ਗੁੱਡ ਨਾਈਟ 🥱🫢**",
"**ਸੋਜੋਂ ਜੀ 🤗😴**",
"**ਰਾਤ ਹੋਗੀ ਜੀ ਨਿਨਿ ਕਰਲੋ 💘😚**",
"**ਤੁਸੀ ਹਲੇ ਸੁੱਤੇ ਨਹੀਂ 🙀😾**",
"**ਹਾਂਜੀ ਕਦੋ ਸੌਣਾ ਫੇਰ 👀🫶🏻**",
"**ਰਖਦੋ ਫੋਨ ਸੋਜੋ ਛੇਤੀ 💘😘**",
"**ਛੇਤੀ ਸੋਜਯੋ ਨਹੀਂ ਤੇ ਮਾਉ ਆਜੁ 🙀👽**",
"**ਤੁਸੀ ਕਦੋ ਸੋਵੋਗੇ 😢😮‍💨**",
"**ਗੁੱਡ ਨਾਈਟ ਜੀ 💘 ਬਬ ਜੂ 🤗**",
]


VC_TAG = [ "**ਆਜੋ ਗਾਣੇ ਸੁਣਦੇ ਆ 😺🌜**",

"**ਵੀਸੀ ਆਜੋ ਗਲਾ ਕਰੀਏ 😚🫶🏻**",

"**ਮੇ ਕਲਾ vc ਬੈਠਾ ਤੁਸੀ ਵੀ ਆਜੋ 😿🤗**",

"**ਤੁਹਾਡਾ ਦਿਲ ਨਹੀਂ ਕਰਦਾ ਮੇਰੇ ਨਲ ਗਲ ਕਰਨ ਨੂੰ 🥲🕊️ vc ਆਓ ☹️**",

"**VC ਅਉ ਤੁਹਾਡੀ ਪਸੰਦ ਦੇ ਗਾਣੇ ਲੋਣਾ 👻🤠🙈**",

"**ਉਤੇ VC ਆਓ 😺ਤੇ ਪਾਓ ਮੇਰੀ ਵਾਜ ਸੁਣਨ ਦਾ ਮੌਕਾ 🙈💘**",

"**ਜੱਟ ਕਲਾ vc ਬੈਠਾ 😮‍💨 ਕੋਈ ਜੱਟੀ ਆਜੋ**",

"**ਨਿ ਤੇਰੀ ਵਾਜ ਸੁਣਨ ਲਈ ਤਰਸੇ ਆ 🙈🥲 VC ਗੇੜਾ ਮਾਰ ਕੁੜੇ 😜🫠**",

"**VC ਆਓ ਤੇ ਪਾਓ 100 % ਕੈਸ਼ ਬੈਕ 👻😼**",
]

CHAT_TAG = [ "**ਤੁਸੀ ਕਿੱਥੇ ਓ 👀☹️**",

"**ਆਜੋ ਗਲਾ ਕਰੀਏ 😺🫠**",

"**ਕੋਈ ਤੇ ਚੈਟ ਕਰਨ ਨੁ ਆਜੋ 🕊️🥲**",

"**ਕਿੱਥੇ ਓ 𝐁𝐔𝐒𝐘 ਬੰਦਿਓ 🌜🌛**",

"**ਤੁਸੀ ਕਿੱਥੇ ਓ 🥲 ਮੇ ਉਡੀਕ ਕਰ ਕੇ ਥੱਕ ਗਿਆ 😾**",

"**ਤੁਸੀ ਗਲਾ ਕਰਦੇ ਨਹੀਂ 😮‍💨 ਅਸੀ ਵਾਕੇ ਕਰਨੇ ਆ 😾**",

"**ਆਜਾ ਛੇੜੀਏ ਬਾਤੜੀਆ 🙈 ਬੋਹਤੀ ਦੇਰ ਨਾ ਲਾਯੋ ਜੀ 💘**",

"**ਦਿੱਲ ਕਰੇ ਤੇਰੇ ਨਲ ਗਲ ਕਰਨ ਦਾ 💞 grp ਦੇ ਵਿਚ ਗੇੜਾ ਮਾਰ ਕੁੜੇ 🕊️**",

"**𝐆𝐑𝐏 ਚ ਆਓਗੇ 💘 ਕੇ 𝐃𝐌 ਕਰਲੀਏ**",

"** ਆਜਾ ਮੇਰੇ ਬਟੁਰੇ 🤭ਕਿੱਥੇ ਰਹਿ ਗਿਆ❤️ **",
            
"** ਬਾਹ ਫੜ੍ਹ 🫣 ਤੈਨੂੰ ਗੇੜਾ ਲਵਾਇਏ ਗਰੁੱਪ ਦਾ😜 **",
            
"** ਆ ਗੰਦਾ 😕 ਜਿਹਾ ਗਲੂਪ ਆ ਇਥੇ ਆਜੋ 🙈[ @PBXCHATS | @PB_1O1 ] 😚 **",
            
"** ਮੇਰਾ ਨੋਨਾ 😍 ਓਨਵਰ [ @BadMundaXD ] 🥰 **",
            
"** ਆਜਾ ਬਾਤਾ 😚ਪਾਈਏ ਰਲਕੇ 👻 **",
            
"** ਅਕੜ ਬਕੜ ⚡ ਬੰਬੇ ਬੌ ਆਜਾ ਜਮੀਏ ਆਪਣੇ ਨਿਆਣੇ ਦੋ🙉 **",
            
"** ਆਜਾ ਚੰਦਰੀਏ 🙊 ਭੜਿਕੇ ਪਾਈਏ ਦਿਲਾ ਦੇ ❤️ **",
            
"** ਦੂਜੇ ਗਰੁੱਪਾਂ 😒ਚ ਕਿ ਕਰਦੀ ਇੱਥੇ ਵੀ ਫੇਰਾ ਪਾਜਾ 😕 **",
            
"** ਆਜਾ ਬੇਬੀ ਬੋਰੀਅਤ 🤓 ਦੀ ਜੜ ਤੋੜੀਏ ਦੋਵੇਂ ਰਲਕੇ ਗੱਲਾਂ ਅੱਗੇ ਤੋਰੀਏ 🥳 **",
            
"** ਆਜਾ ਪਾਂ ਲੀਏ ਜੇਬੀ 🌹 ਚ ਤੇਨੂੰ ਕਿੱਥੇ ਭਜਦੀ 🐒 **",
            
"** ਚਲ ਛਿਪ ਗਿਆ 🌚 ਚੰਨ ਹੋ ਗਿਆ ਸਵੇਰਾ ਪਾਂ ਜਾ ਮੇਰੇ ਸੁਪਨਿਆਂ ਚ ਫੇਰਾ 👻 **",  

"** ਆਜਾ ਮੇਰੀ ਬੁਲਬੁਲ ਪਿਆਰ ਦੀਆ ਬਾਤਾ ਪਾਈਏ 🙈❤️ **",

"** ਉਰੇ ਆ ਤੇਰੇ ਕੰਨ ਚ ਇਕ ਗਲ ਕਹਿਣੀ 🙊😜 **",

"** ਥੋਨੂੰ ਮੇਰੀ ਯਾਦ ਨਹੀਂ ਆਉਂਦੀ 🥺❤️‍🩹 **",

"** ਇਕ ਤੁ ਹੋਵੇ , ਇਕ ਮੇ ਹੋਵਾ - ਮੈਨੂੰ ਨਲ ਰੱਖੇ , ਮੇਰਾ ਜੀ ਕਰਦੇ 🫣❤️ **",

"** ਆਜਾ ਜੀ 💗 ਦਿਲ ਬੇਚੈਨ ਆ ਤੇਰੇ ਇਕ msg ਲਈ 🫠**",

"** ਕਿੱਥੇ ਗੁਮ ਹੋ ਗਿਆ 😿 ਦਿਲ ਤੇਰਾ ਮੈਂ ਰਾਹ ਤੱਕਦਾ ਰਹਿ ਗਿਆ 💞**",

"** ਗਰੁੱਪ ਸੁੰਨਾ ਲੱਗਦਾ 😕 ਜਦ ਤੂੰ ਨਹੀਂ ਹੁੰਦੀ 💘**",

"** ਥੋੜ੍ਹੀ ਗੱਲ ਕਰ ਲੈ 😽 ਦਿਲ ਨੂੰ ਸਕੂਨ ਮਿਲ ਜਾਊ 💕**",

"** ਬਿਨਾਂ ਤੇਰੇ 😕 ਗਰੁੱਪ ਵੀ ਅਜੀਬ ਲੱਗਦਾ 💔**",

"** ਆਜਾ ਤੇਰੇ ਆਉਂਦੇ ਹੀ 😍 ਗਰੁੱਪ ਚ ਰੌਣਕ ਆ ਜਾਊ 🌸**",

"** ਥੱਕਿਆ ਦਿਲ 🥺 ਤੇਰੇ ਦੋ MSG ਦੀ ਉਡੀਕ ਕਰਦਾ 💞**",

"** ਤੇਰੇ ਬਿਨਾ 😔 ਦਿਲ ਨਹੀਂ ਲੱਗਦਾ, ਆ ਗੱਲਾਂ ਦੀ ਝੜੀ ਲਾਈਏ 🌧️**"

"** ਆਜਾ ਜੀ 💓 ਦਿਲ ਅੱਜ ਕੁਝ ਜ਼ਿਆਦਾ ਹੀ ਤੇਰੇ ਲਈ ਧੜਕ ਰਿਹਾ 🫠**",

"** ਤੇਰੇ ਬਿਨਾਂ 😔 ਗੱਲਾਂ ਵੀ ਅਧੂਰੀਆਂ ਨੇ, ਗਰੁੱਪ ਵੀ ਸੁੰਨਾ 💔**",

"** ਤੇਰਾ msg 😍 ਆਵੇ ਤਾਂ ਦਿਨ ਬਣ ਜਾਵੇ 💌**",

"** ਆਜਾ ਸੋਹਣੀਏ 🫶 ਗੱਲਾਂ ਨਾਲ ਦਿਲਾਂ ਦੀ ਦੂਰੀ ਘਟਾਈਏ 💖**",

"** ਆਜਾ ਜਾਨ 💓 ਗਰੁੱਪ ਨੂੰ ਵੀ ਤੇਰੀ ਲੋੜ ਆ, ਤੇ ਦਿਲ ਨੂੰ ਵੀ 😌**",

"** ਤੇਰੇ ਬਿਨਾਂ 🌚 ਰਾਤ ਵੀ ਰਾਤ ਨਹੀਂ ਲੱਗਦੀ 💔**",

"** ਗਰੁੱਪ ਚ ਰੌਣਕ 😍 ਤੇਰੇ ਆਉਂਦੇ ਨਾਲ ਹੀ ਆਉਂਦੀ 🌸**",

"** ਥੋੜ੍ਹਾ ਟਾਈਮ ਕੱਢ ਲੈ 🥺 ਮੇਰੇ ਦਿਲ ਦੇ ਲਈ 💓**",

"** ਆਜਾ ਅੱਜ 💫 ਦਿਲ ਨਾਲ ਦਿਲ ਜੋੜੀਏ 😚**",
] 

@on_message("pgmtag", allow_stan=True, Bad_user=True)
async def mention_allvc(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("๏ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴘs.")

    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("๏ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ, ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴛᴀɢ ᴍᴇᴍʙᴇʀs. ")
    if chat_id in spam_chats:
        return await message.reply("๏ ᴘʟᴇᴀsᴇ ᴀᴛ ғɪʀsᴛ sᴛᴏᴘ ʀᴜɴɴɪɴɢ ᴍᴇɴᴛɪᴏɴ ᴘʀᴏᴄᴇss...")
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}) "

        if usrnum == 1:
            txt = f"{usrtxt} {random.choice(GM_TAG)}"
            await client.send_message(chat_id, txt)
            await asyncio.sleep(4)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass



@on_message("pgmstop", allow_stan=True, Bad_user=True)
async def cancel_spam(client, message):
    if not message.chat.id in spam_chats:
        return await message.reply("๏ ᴄᴜʀʀᴇɴᴛʟʏ ɪ'ᴍ ɴᴏᴛ ᴛᴀɢɢɪɴɢ ʙᴀʙʏ.")
    is_admin = False
    try:
        participant = await client.get_chat_member(message.chat.id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("๏ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ, ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴛᴀɢ ᴍᴇᴍʙᴇʀs.")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.reply("๏ ᴍᴇɴᴛɪᴏɴ ᴘʀᴏᴄᴇss sᴛᴏᴘᴘᴇᴅ ๏")

#gntag

@on_message("pgntag", allow_stan=True, Bad_user=True)
async def mention_allvc(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("๏ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴘs.")

    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("๏ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ, ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴛᴀɢ ᴍᴇᴍʙᴇʀs. ")
    if chat_id in spam_chats:
        return await message.reply("๏ ᴘʟᴇᴀsᴇ ᴀᴛ ғɪʀsᴛ sᴛᴏᴘ ʀᴜɴɴɪɴɢ ᴍᴇɴᴛɪᴏɴ ᴘʀᴏᴄᴇss...")
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}) "

        if usrnum == 1:
            txt = f"{usrtxt} {random.choice(GN_TAG)}"
            await client.send_message(chat_id, txt)
            await asyncio.sleep(4)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass



@on_message("pgnstop", allow_stan=True, Bad_user=True)
async def cancel_spam(client, message):
    if not message.chat.id in spam_chats:
        return await message.reply("๏ ᴄᴜʀʀᴇɴᴛʟʏ ɪ'ᴍ ɴᴏᴛ ᴛᴀɢɢɪɴɢ ʙᴀʙʏ.")
    is_admin = False
    try:
        participant = await client.get_chat_member(message.chat.id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("๏ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ, ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴛᴀɢ ᴍᴇᴍʙᴇʀs.")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.reply("๏ ᴍᴇɴᴛɪᴏɴ ᴘʀᴏᴄᴇss sᴛᴏᴘᴘᴇᴅ ๏")
        
# VC TAG #

@on_message("pvctag", allow_stan=True, Bad_user=True)
async def mention_allvc(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("๏ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴘs.")

    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("๏ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ, ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴛᴀɢ ᴍᴇᴍʙᴇʀs. ")
    if chat_id in spam_chats:
        return await message.reply("๏ ᴘʟᴇᴀsᴇ ᴀᴛ ғɪʀsᴛ sᴛᴏᴘ ʀᴜɴɴɪɴɢ ᴍᴇɴᴛɪᴏɴ ᴘʀᴏᴄᴇss...")
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}) "

        if usrnum == 1:
            txt = f"{usrtxt} {random.choice(VC_TAG)}"
            await client.send_message(chat_id, txt)
            await asyncio.sleep(4)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass



@on_message("pvcstop", allow_stan=True, Bad_user=True)
async def cancel_spam(client, message):
    if not message.chat.id in spam_chats:
        return await message.reply("๏ ᴄᴜʀʀᴇɴᴛʟʏ ɪ'ᴍ ɴᴏᴛ ᴛᴀɢɢɪɴɢ ʙᴀʙʏ.")
    is_admin = False
    try:
        participant = await client.get_chat_member(message.chat.id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("๏ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ, ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴛᴀɢ ᴍᴇᴍʙᴇʀs.")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.reply("๏ ᴍᴇɴᴛɪᴏɴ ᴘʀᴏᴄᴇss sᴛᴏᴘᴘᴇᴅ ๏")

# CHAT TAG #

@on_message("ptag", allow_stan=True, Bad_user=True)
async def mention_allvc(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("๏ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴘs.")

    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("๏ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ, ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴛᴀɢ ᴍᴇᴍʙᴇʀs. ")
    if chat_id in spam_chats:
        return await message.reply("๏ ᴘʟᴇᴀsᴇ ᴀᴛ ғɪʀsᴛ sᴛᴏᴘ ʀᴜɴɴɪɴɢ ᴍᴇɴᴛɪᴏɴ ᴘʀᴏᴄᴇss...")
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}) "

        if usrnum == 1:
            txt = f"{usrtxt} {random.choice(CHAT_TAG)}"
            await client.send_message(chat_id, txt)
            await asyncio.sleep(4)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass



@on_message("pstop", allow_stan=True, Bad_user=True)
async def cancel_spam(client, message):
    if not message.chat.id in spam_chats:
        return await message.reply("๏ ᴄᴜʀʀᴇɴᴛʟʏ ɪ'ᴍ ɴᴏᴛ ᴛᴀɢɢɪɴɢ ʙᴀʙʏ.")
    is_admin = False
    try:
        participant = await client.get_chat_member(message.chat.id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("๏ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ, ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴛᴀɢ ᴍᴇᴍʙᴇʀs.")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.reply("๏ ᴍᴇɴᴛɪᴏɴ ᴘʀᴏᴄᴇss sᴛᴏᴘᴘᴇᴅ ๏")
        

HelpMenu("tag").add(
    "pgmtag", None, "Ptag All (GM Style) 🌅"
).add(
    "pgmstop", None, "Pstop GM Style Tagging ❌"
).add(
    "pgntag", None, "Ptag All (GN Style) 🌃"
).add(
    "pgnstop", None, "Pstop GN Style Tagging ❌"
).add(
    "pvctag", None, "Ptag All (VC Style) 🎙️"
).add(
    "pvcstop", None, "Pstop VC Style Tagging ❌"
).add(
    "ptag", None, "Ptag All (Chat Style) 💬"
).add(
    "pstop", None, "Stop Chat Tagging ❌"
).info("Reply to a message or use normally in group").done()
