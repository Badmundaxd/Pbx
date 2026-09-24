import random
import asyncio

from pyrogram import Client, filters
from pyrogram.enums import ChatAction as CA
from pyrogram.types import Message

from . import *

RAID_STR = [
    "मादरचोद तेरी माँ की चूत में घुटका खाके थूक दूंगा 🤣🤣",
    "तेरे बहन की चूत में चाकू डाल कर चूत का खून कर दूँगा",
    "तेरी वहीं नहीं है क्या? 9 महीने रुक सगी वहीं देता हूं 🤣🤣🤩",
    "तेरी मां के भोसड़े में एयरोप्लेन पार्क करके उड़ान भर दूंगा ✈️🛫",
    "तेरी मां की चूत में सुतली बम फोड़ दूंगा तेरी माँ की झाटे जल के खाक हो जाएगी 💣",
    "तेरी माँ की चूत में स्कूटर डाल दूँगा 👅",
    "तेरी माँ की चूत काटके गली के कुत्तों को बाँट दूँगा 🦮 फिर ब्रेड की तरह खाएँगे 🍞",
    "दूध हिलाऊंगा तेरी वहीं के ऊपर नीचे 🆙🆒😙",
    "तेरी मां की चूत में हाथ डालके बच्चे निकाल दूंगा 😍",
    "तेरी बहन की चूत में केले के छिलके 🍌🍌😍",
    "तेरी बहन की चूत में यूजरबोट लगाऊंगा सस्ते स्पैम के लिए",
    "तेरी वहीं धंधे वाली 😋😛",
    "तेरी मां के भोसड़े में AC लगा दूंगा सारी गर्मी निकल जाएगी",
    "तेरी वहीं को हॉर्लिक्स पिलाऊंगा मादरचोद 😚",
    "तेरी मां की गांड में सरिया डाल दूंगा उसपे टांग के बच्चे पैदा होंगे 😱😱",
    "तेरी मां को कोलकाता वाले जीतू भैया का लंड मुबारक 🤩🤩",
    "तेरी मम्मी की फैंटसी हूं लौड़े, तू अपनी बहन संभाल 😈😈",
    "तेरा पहला बाप हूं मादरचोद",
    "तेरी वहीं के भोसड़े में XVIDEOS.COM चला के मुठ मारूंगा 🤡😹",
    "तेरी मां का ग्रुप वालों साथ गैंगबैंग करूंगा 🙌🏻☠️",
    "तेरी आइटम की गांड में लंड डालके तेरे जैसा एक और निकाल दूंगा 🤘🏻☠️",
    "औकात में रह वरना गांड में डंडा डाल के मुंह से निकाल दूंगा 🙄🤭",
    "तेरी मम्मी के साथ लूडो खेलते उसके मुंह में लोडा दे दूंगा ☝🏻😬",
    "तेरी वहीं को लंड पर इतना झुलाऊंगा बच्चा पैदा कर देगी 👀👯",
    "तेरी मां की चूत में बैटरी लगा के पावरबैंक बना दूंगा 🔋🤩",
    "तेरी मां की चूत में C++ एन्क्रिप्शन लगा दूंगा लीक होना बंद 😈🔥",
    "तेरी मां की गांड में झाड़ू डाल के मोर बना दूंगा 🦚🥵",
    "तेरी चूत में शोल्डरिंग कर दूंगा हिलते हुए भी दर्द होगा 🤮👺",
    "तेरी मां को रेडी पर बैठा के चूत बिलवाऊंगा 💰😵",
    "भोसदीके तेरी मां की चूत में 4 छेद हैं, मसील लगा के भी बहती है 👊🤢",
    "तेरी बहन की चूत में बरगद का पेड़ उगा दूंगा, सब ऑक्सीजन लेंगे 🤢🥳",
    "तेरी मां की चूत में सूडो + बिगस्पैम चला के 9999 फक दूंगा 🤩🔥",
    "तेरी बहन के भोसड़े में बेसन लड्डू भर दूंगा 😈",
    "तेरी मां की चूत खोद के सिलेंडर फिट करके दाल मखनी बनाऊंगा ⛽️🔥",
    "तेरी मां की चूत में क्रेडिट कार्ड डाल के 500 के नोट निकालूंगा 💰🤩",
    "तेरी मां के साथ सूअर का सेक्स करवाऊंगा, 6-6 बच्चे देगी 🔥😱",
    "तेरी बहन की चूत में Apple 18W चार्जर 🔥🤩",
    "तेरी बहन की गांड में OnePlus Warp 30W 💥😎",
    "तेरी बहन की चूत Amazon से 10₹ में ऑर्डर करके Flipkart पे 20₹ में बेच दूंगा 🤮👿",
    "तेरी मां की भुंड में Zomato से Subway BFF सब ऑर्डर कर COD, 9 महीने बाद फ्री डिलीवरी 🙀🥳",
    "तेरी बहन की चूत काली 🙁🤣",
    "तेरी मां की चूत में कमिट करूंगा, तेरी बहन की चूत auto-update हो जाएगी 🤖",
    "तेरी मौसी के भोसड़े में इंडियन रेलवे 🚂😂",
    "तू, तेरी बहन, तेरा खानदान – सब रंडी के बच्चे 🤢🔥",
    "तेरी बहन की चूत में ionic bond बना के virginity लूज करवा दूंगा 📚😎",
    "तेरी रंडी मां से पूछ बाप का नाम, बहन के लौड़े 🤩😳",
    "तेरी मां को इतना चोदूंगा तेरा बाप भी पहचानने से मना कर देगा 😂👿",
    "तेरी बहन के भोसड़े में हेयर ड्रायर चला दूंगा 🔥",
    "तेरी मां की चूत में Telegram की सारी रंडियों का खाना खोल दूंगा 👿😎",
    "तेरी मां की चूत में Alexa डाल के DJ बजाऊंगा 🎶🤩",
    "तेरी मां के भोसड़े में GitHub डाल के अपना बॉट होस्ट करूंगा 👊😍",
    "तेरी बहन का VPS बना के 24/7 bash चुदाई कमांड दूंगा 🔥",
    "तेरी मम्मी की चूत में तेरा लंड डाल के काट दूंगा 🔪😂",
    "सुन तेरी मां का भोसड़ा और तेरी बहन का भी 👿👊",
    "तुझे देख के तेरी रंडी बहन पे तरस आता है बहन के लौड़े 💥🔥",
    "सुन मादरचोद ज्यादा उछल मत, एक मिनट में मां चोद दूंगा ✅🤣",
    "अपनी अम्मा से पूछ काली रात में कौन चोदने आया था? 😂😳",
    "तेरी मां के भोसड़े में Spotify डाल के लोफी बजाऊंगा दिन भर 🎶😍",
    "तेरी मां का नया रंडीखाना खोलूंगा, चिंता मत कर 👊🤣",
    "तेरा बाप हूं भोसदीके, तेरी मां को रंडीखाने पे चुदवा के दारू पीता हूं 🍷🔥",
    "तेरी बहन की चूत में अपना मोटा लौड़ा घुसा के कलाप के मार दूंगा 🤩😳",
]

COLLECTION_NAME = "hindi_raid_targets"

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

@custom_handler(filters.all & ~filters.private, group=-17)
async def hindi_reply_raid_handler(c: Client, m: Message):
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

@on_message("hreplyraid", allow_stan=True)
async def activate_hreplyraid(c: Client, m: Message):
    bot_id = c.me.id
    if m.reply_to_message and m.reply_to_message.from_user:
        target_user = m.reply_to_message.from_user
    else:
        try:
            target_user = await c.get_users(m.command[1])
        except:
            return await Pbxbot.delete(m, "`Reply to a user or provide username/ID.`")
    if target_user.is_self or target_user.id in Config.DEVS:
        return await Pbxbot.delete(m, "`Can't raid myself or devs.`")
    username = f"@{target_user.username}" if target_user.username else target_user.mention
    msg = await m.reply_text("`Activating Hindi Reply Raid...`")
    if await is_raid_active(bot_id, target_user.id):
        return await msg.edit(f"`Reply raid already active on {username}`")
    await add_raid_target(bot_id, target_user.id)
    await msg.edit(f"**✅ Hindi Reply Raid Activated on {username}**")

@on_message("dhreplyraid", allow_stan=True)
async def deactivate_hreplyraid(c: Client, m: Message):
    bot_id = c.me.id
    if m.reply_to_message and m.reply_to_message.from_user:
        target_user = m.reply_to_message.from_user
    else:
        try:
            target_user = await c.get_users(m.command[1])
        except:
            return await Pbxbot.delete(m, "`Reply to a user or provide username/ID.`")
    username = f"@{target_user.username}" if target_user.username else target_user.mention
    msg = await m.reply_text("`Deactivating Hindi Reply Raid...`")
    if not await is_raid_active(bot_id, target_user.id):
        return await msg.edit(f"`No active reply raid on {username}`")
    await remove_raid_target(bot_id, target_user.id)
    await msg.edit(f"**❌ Hindi Reply Raid Deactivated on {username}**")

HelpMenu("hindireplyraid").add(
    "hreplyraid", "<reply/username/id>", "Start Hindi reply raid.", "hreplyraid @username"
).add(
    "dhreplyraid", "<reply/username/id>", "Stop Hindi reply raid.", "dhreplyraid @username"
).info("Hindi Reply Raid Module").done()
