import random
import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from . import *

RAID_STR = [
    "MADARCHOD TERI MAA KI CHUT ME GHUTKA KHAAKE THOOK DUNGA 🤣🤣",
    "TERE BEHEN K CHUT ME CHAKU DAAL KAR CHUT KA KHOON KAR DUGA",
    "TERI VAHEEN NHI HAI KYA? 9 MAHINE RUK SAGI VAHEEN DETA HU 🤣🤣🤩",
    "TERI MAA K BHOSDE ME AEROPLANEPARK KARKE UDAAN BHAR DUGA ✈️🛫",
    "TERI MAA KI CHUT ME SUTLI BOMB FOD DUNGA TERI MAA KI JHAATE JAL KE KHAAK HO JAYEGI 💣",
    "TERI MAAKI CHUT ME SCOOTER DAAL DUGA 👅",
    "TERI MAA KI CHUT KAKTE GALI KE KUTTO ME BAAT DUNGA PHIR BREAD KI TARH KHAYENGE 🦮🍞",
    "DUDH HILAAUNGA TERI VAHEEN KE UPR NICHE 🆙🆒😙",
    "TERI MAA KI CHUT ME HATTH DALKE BACCHE NIKAL DUNGA 😍",
    "TERI BEHN KI CHUT ME KELE KE CHILKE 🍌🍌😍",
    "TERI BHEN KI CHUT ME USERBOT LAGAAUNGA SASTE SPAM KE CHODE",
    "TERI VAHEEN DHANDHE VAALI 😋😛",
    "TERI MAA KE BHOSDE ME AC LAGA DUNGA SAARI GARMI NIKAL JAAYEGI",
    "TERI VAHEEN KO HORLICKS PEELAUNGA MADARCHOD 😚",
    "TERI MAA KI GAAND ME SARIYA DAAL DUNGA USI PR TANG KE BACHE PAIDA HONGE 😱😱",
    "TERI MAA KO KOLKATA VAALE JITU BHAIYA KA LUND MUBARAK 🤩🤩",
    "TERI MUMMY KI FANTASY HU LAWDE, TU APNI BHEN KO SMBHAAL 😈😈",
    "TERA PEHLA BAAP HU MADARCHOD",
    "TERI VAHEEN KE BHOSDE ME XVIDEOS.COM CHALA KE MUTH MAARUNGA 🤡😹",
    "TERI MAA KA GROUP VAALON SAATH GANG BANG KRUNGA 🙌🏻☠️",
    "TERI ITEM KI GAAND ME LUND DAALKE TERE JAISA EK OR NIKAAL DUNGA 🤘🏻☠️",
    "AUKAAT ME REH VRNA GAAND ME DANDA DAAL KE MUH SE NIKAAL DUNGA 🙄🤭",
    "TERI MUMMY KE SAATH LUDO KHELTE USKE MUH ME LODA DE DUNGA ☝🏻😬",
    "TERI VAHEEN KO LUND PR JHULAAUNGA JHULTE HI BACHA PAIDA KR DEGI 👀👯",
    "TERI MAA KI CHUT ME BATTERY LAGA KE POWERBANK BANA DUNGA 🔋🤩",
    "TERI MAA KI CHUT ME C++ ENCRYPTION LAGA DUNGA RUK JAYEGI 😈🔥",
    "TERI MAA KE GAAND ME JHAADU DAL KE MOR BANA DUNGAA 🦚🥵",
    "TERI CHUT ME SHOULDERING KAR DUNGA HILTE BHI DARD HOGA 🤮👺",
    "TERI MAA KO REDI PE BAITHAL KE CHUT BILWAUNGAA 💰😵",
    "BHOSDIKE TERI MAA KI CHUT ME 4 HOLE HAI MSEAL LAGA KE BHI BAHETI HAI 👊🤢",
    "TERI BAHEN KI CHUT ME BARGAD KA PED UGA DUNGA OXYGEN LEKAR JAYENGE 🤢🥳",
    "TERI MAA KI CHUT ME SUDO + BIGSPAM 9999 FUCK LAGAA DU 🤩🔥",
    "TERI VAHEN KE BHOSDIKE ME BESAN KE LADDU BHAR DUNGA 😈",
    "TERI MAA KI CHUT KHOD KE CYLINDER FIT KARKE DAL MAKHANI BANAUNGAAA ⛽️🔥",
    "TERI MAA KI CHUT ME SHEESHA DAL KE CHAURAHE PE TAANG DUNGA 😈🤩",
    "TERI MAA KI CHUT ME CREDIT CARD DAL KE 500 KE NOTE NIKALUNGAA 💰🤩",
    "TERI MAA KE SATH SUAR KA SEX KARWAUNGA 6-6 BACHE DEGI 🔥😱",
    "TERI BAHEN KI CHUT ME APPLE 18W CHARGER 🔥🤩",
    "TERI BAHEN KI GAAND ME ONEPLUS WRAP 30W 💥😎",
    "TERI BAHEN KI CHUT AMAZON SE 10RS ORDER FLIPKART PE 20RS BECH DUNGA 🤮👿",
    "TERI MAA KI BHUND ME ZOMATO SUBWAY COMBO COD – 9 MONTH BAAD FREE DELIVERY 🙀🥳",
    "TERI BHEN KI CHUT KAALI 🙁🤣",
    "TERI MAA KI CHUT ME COMMIT KARUNGA TERI BHEN KI AUTO UPDATE 🤖",
    "TERI MAUSI KE BHOSDE ME INDIAN RAILWAY 🚂😂",
    "TU TERI BAHEN TERA KHANDAN SAB RANDI KE BACHE 🤢🔥",
    "TERI BAHEN KI CHUT ME IONIC BOND BANA KE VIRGINITY LOOT LUNGA 📚😎",
    "TERI RANDI MAA SE PUCH BAAP KA NAAM 🤩😳",
    "TU AUR TERI MAA DONO KI BHOSDE ME METRO CHALWA DUNGA 🚇🥶",
    "TERI MAA KO ITNA CHODUNGA TERA BAAP PAHCHANNE SE MANA KAREGA 😂👿",
    "TERI BAHEN KE BHOSDE ME HAIR DRYER CHALA DUNGAA 🔥",
    "TERI MAA KI CHUT ME TELEGRAM RANDI KHANA KHOL DUNGAA 👿😎",
    "TERI MAA KI CHUT ME ALEXA DAL KE DJ BAJAUNGAAA 🎶🤩",
    "TERI MAA KE BHOSDE ME GITHUB DAL KE BOT HOST KARUNGAA 👊😍",
    "TERI BAHEN KA VPS BANA KE 24*7 BASH CHUDAI COMMAND 🔥",
    "TERI MUMMY KI CHUT ME TERA LAND DAL KE KAAT DUNGA 🔪😂",
    "SUN TERI MAA AUR BAHEN KA BHOSDA 👿👊",
    "TUJHE DEKH KE TERI RANDI BAHEN PE TARAS AATA HAI 💥🔥",
    "SUN MADARCHOD JYADA UCHAL MAT EK MIN ME MAA CHOD DUNGA ✅🤣",
    "APNI AMMA SE PUCH KAUN CHODNE AAYA THA KAALI RAAT ME 😂😳",
    "TERI MAA KE BHOSDE ME SPOTIFY DAL KE LOFI DIN BHAR 😍🎶",
    "TERI MAA KA NAYA RANDI KHANA KHOLUNGA 👊🤣",
    "TERA BAAP HU – TERI MAA KO CHUDWA KE DAARU PEETA HU 🍷🔥",
    "TERI BAHEN KI CHUT ME BADA LODA GHUSSA KE MAR DUNGA 🤩😳",
    "KINGFISHER BOTTLE TERI MUMMY KI CHUT ME TOD DUNGA 😱😂",
    "TERI MAA KO ITNA CHODUNGA SAPNE ME BHI YAAD KAREGI 🥳😍",
    "DAUDA DAUDA KE TERI MUMMY BAHEN CHODUNGA 😎🤣",
    "TERI MUMMY KI CHUT OLX PE BECH KE TERI BAHEN KA KOTHA KHOLUNGA 😝😍",
    "TERI MAA KE BHOSDA MAST CHODUNGA TU DUR NHI JA PAYEGA 😏🤩",
    "APNI BAHEN SE SEEKH KAISE GAAND MARWATE HAI 😏🤬",
    "TERI MAA KA YAAR TERI BAHEN KA PYAAR – LAND CHOOS 🤩💥",
    "MADARCHOD",
    "BHOSDIKE",
    "LAAAWEEE KE BAAAAAL",
    "MAAAAR KI JHAAAAT KE BBBBBAAAAALLLLL",
    "MADRCHOD",
    "TERI MA KI CHUT",
    "LWDE KE BAAALLL",
    "MACHAR KI JHAAT",
    "TERI MA KA BHOSDAA",
    "TERI BHN BDI RANDI",
    "TERI MA OSSE BADI RAND",
    "TERA BAAP CHKAAAA",
    "KITNI CHODU TERI MA",
    "TERI MA CHOD DI",
    "TERI MA KE STH REELS ROAD PE",
    "TERI MA KI CHUT TOP SEXY",
    "SPEED PKD LWDEEEE",
    "BAAP KI SPEED MATCH KRR",
    "PAPA KI SPEED NHI HO RHI?",
    "CHUD GYA PAPA SEEE",
    "SALE RAPE KAR DUNGA",
    "HAHAHAAAAA",
    "KIDSSSS",
    "TERI MA CHUD GYI",
    "BHEN KE LWDE SHRM KR",
    "KITNI GALIYA PADWAYEGA APNI MA KO",
    "SHRM KR",
    "MERE LUND KE BAAAAALLLLL",
    "RNDI KE LDKEEEEEEEEE",
    "Apni gaand mein muthi daal",
    "Apni lund choos",
    "Apni ma ko ja choos",
    "Bhen ke laude",
    "TERI MA SBSE BDI RAND",
    "KASH MUTH MARKE SOJA TUN PAIDA NA HOTA",
    "GLTI KRDI TUJHE PAIDA KRKE",
    "Gaand mein bambu DEDUNGAAAAAA",
    "Hazaar lund teri gaand main",
    "TERI MA KI KALI CHUT",
    "Kutte ka awlat",
    "TERI MA RNDIIIIIIIIIIIIIIIIIIII",
    "muh mei lele",
    "MERE LWDE KE BAAAAALLL",
    "CHUD GYAAAAA",
    "Randi khanE KI ULADDD",
    "Teri gaand main kute ka lund",
    "Teri maa ka bhosda",
    "Teri maa ki chut",
    "SUNN MADERCHOD",
    "TERI MAA KA BHOSDA",
    "BEHEN K LUND",
    "MERA LAWDA LELE",
    "GAANDU",
    "CHUTIYA",
    "TERI MAA KI CHUT PE JCB",
    "TERI BEHEN ROZ LETI HAI",
    "TU CHUTIYA TERA KHANDAAN CHUTIYA",
    "TERIIIIII MAAAA KI CHUTTT ME ABCD LIKH DUNGA",
    "RANIDIII",
    "CHODU",
    "RANDI KE PILLE",
    "TERIIIII MAAA KO BHEJJJ",
    "TERAA BAAAAP HU",
    "TERI MAA KO SARAK PE LETAA DUNGA",
    "TERI MAA KO GB ROAD PE BECH DUNGA",
    "TERI MAA SASTI RANDI HAI",
    "TERI MAAA RANDI HAI",
    "TERI MAA KO BISTAR PE LETAAKE CHODUNGA",
    "TERI MAA KO AMERICA GHUMAAUNGA",
    "TERI MAA KI CHUT ME NAARIYAL PHOR DUNGA",
    "TERI MAAA KO HORLICKS PILAUNGA",
    "MERAAA LUND PAKAD LE",
    "TERIII MAA CHUF GEYII",
    "MADARXHODDD",
    "TERIIIIII BEHENNNN KO CHODDDUUUU",
    "NIKAL MADARCHOD",
    "RANDI KE BACHE",
    "TERI SEXY BAHEN KI CHUT OP",
]

COLLECTION_NAME = "mixed_raid_targets"

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

@custom_handler(filters.all & ~filters.private, group=-16)
async def mixed_reply_raid_handler(c: Client, m: Message):
    if not m.from_user:
        return
    bot_id = c.me.id
    user_id = m.from_user.id
    if not await is_raid_active(bot_id, user_id):
        return
    message = random.choice(RAID_STR)
    # Fast reply — no sleep delay
    await m.reply_text(message)

@on_message("replyraid", allow_stan=True)
async def activate_replyraid(c: Client, m: Message):
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
    msg = await m.reply_text("`Activating Mixed Reply Raid...`")
    if await is_raid_active(bot_id, target_user.id):
        return await msg.edit(f"`Reply raid already active on {username}`")
    await add_raid_target(bot_id, target_user.id)
    await msg.edit(f"**✅ Mixed Reply Raid Activated on {username}**")

@on_message("dreplyraid", allow_stan=True)
async def deactivate_replyraid(c: Client, m: Message):
    bot_id = c.me.id
    if m.reply_to_message and m.reply_to_message.from_user:
        target_user = m.reply_to_message.from_user
    else:
        try:
            target_user = await c.get_users(m.command[1])
        except:
            return await Pbxbot.delete(m, "`Reply to a user or provide username/ID.`")
    username = f"@{target_user.username}" if target_user.username else target_user.mention
    msg = await m.reply_text("`Deactivating Mixed Reply Raid...`")
    if not await is_raid_active(bot_id, target_user.id):
        return await msg.edit(f"`No active reply raid on {username}`")
    await remove_raid_target(bot_id, target_user.id)
    await msg.edit(f"**❌ Mixed Reply Raid Deactivated on {username}**")

HelpMenu("replyraid").add(
    "replyraid", "<reply/username/id>", "Start mixed reply raid.", "replyraid @username"
).add(
    "dreplyraid", "<reply/username/id>", "Stop reply raid.", "dreplyraid @username"
).info("Mixed Reply Raid Module").done()
