import random
import asyncio

from pyrogram import Client, filters
from pyrogram.enums import ChatAction as CA
from pyrogram.types import Message

from . import *

RAID_STR = [
    "MADARCHOD I'LL CHEW GUTKHA AND SPIT IN YOUR MOM'S PUSSY 🤣🤣",
    "I'LL STAB YOUR SISTER'S PUSSY WITH A KNIFE AND MAKE IT BLEED",
    "DON'T YOU HAVE A SISTER? WAIT 9 MONTHS – I'LL GIVE YOU A REAL ONE 🤣🤣🤩",
    "I'LL PARK PLANES IN YOUR MOM'S PUSSY AND TAKE OFF ✈️🛫",
    "I'LL BLOW A SUITCASE BOMB IN YOUR MOM'S PUSSY TILL HER PUBES BURN 💣",
    "I'LL SHOVE A SCOOTER IN YOUR MOM'S PUSSY 👅",
    "I'LL FEED YOUR MOM'S PUSSY HAIR TO STREET DOGS 🦮 THEN THEY'LL EAT IT LIKE BREAD 🍞",
    "I'LL JERK OFF ALL OVER YOUR SISTER UP AND DOWN 🆙🆒😙",
    "I'LL REACH IN YOUR MOM'S PUSSY AND PULL OUT BABIES 😍",
    "BANANA PEELS IN YOUR SISTER'S PUSSY 🍌🍌😍",
    "I'LL INSTALL USERBOT IN YOUR SISTER'S PUSSY FOR CHEAP SPAM",
    "YOUR SISTER IS A PRO WHORE 😋😛",
    "I'LL INSTALL AC IN YOUR MOM'S PUSSY – ALL HEAT GONE",
    "I'LL FEED YOUR SISTER HORLICKS MADARCHOD 😚",
    "I'LL SHOVE REBAR IN YOUR MOM'S ASS AND HANG OFF IT TO KNOCK HER UP 😱😱",
    "YOUR MOM GETS BLESSED BY JITU BHAIYA'S DICK 🤩🤩",
    "I'M YOUR MOMMY'S FANTASY, GO HANDLE YOUR SISTER 😈😈",
    "I WAS YOUR FIRST DAD MADARCHOD",
    "I'LL JACK OFF TO XVIDEOS IN YOUR SISTER'S PUSSY 🤡😹",
    "I'LL GANGBANG YOUR MOM WITH THE GROUP 🙌🏻☠️",
    "I'LL RAM DICK IN YOUR GIRL'S ASS AND PULL OUT ANOTHER ONE LIKE YOU 🤘🏻☠️",
    "STAY IN LANE OR I'LL SHOVE STICK UP YOUR ASS AND OUT YOUR MOUTH 🙄🤭",
    "PLAYING LUDO WITH YOUR MOMMY – I'LL SHOVE MY DICK IN HER MOUTH ☝🏻😬",
    "I'LL SWING YOUR SISTER ON MY DICK TILL SHE GETS PREGNANT 👀👯",
    "I'LL TURN YOUR MOM'S PUSSY INTO A POWERBANK 🔋🤩",
    "I'LL CODE C++ ENCRYPTION IN YOUR MOM'S LOOSE PUSSY – NO MORE LEAKS 😈🔥",
    "I'LL SHOVE BROOM IN YOUR MOM'S ASS AND MAKE A PEACOCK 🦚🥵",
    "I'LL SOLDER YOUR PUSSY – IT'LL HURT EVEN WHEN SHAKING 🤮👺",
    "I'LL PUT YOUR MOM ON THE STREET AND RENT HER HOLES 💰😵",
    "YOUR MOM'S PUSSY HAS 4 HOLES – STILL LEAKS AFTER SEALING 👊🤢",
    "I'LL GROW BANYAN TREE IN YOUR SISTER'S PUSSY – OXYGEN FOR ALL 🤢🥳",
    "I'LL RUN SUDO + BIGSPAM IN YOUR MOM'S PUSSY – 9999 FUCKS 🤩🔥",
    "I'LL FILL YOUR SISTER'S PUSSY WITH BESAN LADDOOS 😈",
    "I'LL DIG YOUR MOM'S PUSSY, FIT CYLINDER AND MAKE DAL MAKHANI ⛽️🔥",
    "I'LL HANG A HOOKAH IN YOUR MOM'S PUSSY AT CROSSROADS 😈🤩",
    "I'LL SLIDE CREDIT CARD IN YOUR MOM'S PUSSY AND PULL 500 NOTES 💰🤩",
    "I'LL MAKE A PIG FUCK YOUR MOM – 6 PIGLETS AT ONCE 🔥😱",
    "APPLE 18W CHARGER IN YOUR SISTER'S PUSSY 🔥🤩",
    "ONEPLUS WARP 30W IN YOUR SISTER'S ASS 💥😎",
    "ORDER YOUR SISTER'S PUSSY ON AMAZON 10₹, SELL ON FLIPKART 20₹ 🤮👿",
    "ZOMATO SUBWAY BFF COMBO IN YOUR MOM'S HUGE PUSSY – FREE DELIVERY AFTER 9 MONTHS 🙀🥳",
    "YOUR SISTER'S PUSSY IS BLACK 🙁🤣",
    "I'LL COMMIT CHANGES IN YOUR MOM'S PUSSY – YOUR SISTER AUTO UPDATES 🤖",
    "INDIAN RAILWAY IN YOUR AUNTY'S PUSSY 🚂😂",
    "YOU, YOUR SISTER, YOUR FAMILY – ALL RANDI KIDS 🤢🔥",
    "I'LL MAKE IONIC BOND IN YOUR SISTER'S PUSSY AND RUIN VIRGINITY 📚😎",
    "ASK YOUR RANDI MOM WHO YOUR REAL DAD IS 🤩😳",
    "I'LL RUN METRO THROUGH YOUR MOM AND YOU MADARCHOD 🚇🥶",
    "I'LL FUCK YOUR MOM SO HARD YOUR DAD WON'T RECOGNIZE HER 😂👿",
    "HAIR DRYER IN YOUR SISTER'S PUSSY 🔥",
    "I'LL OPEN RANDI BROTHEL OF TELEGRAM SLUTS IN YOUR MOM'S PUSSY 👿😎",
    "ALEXA IN YOUR MOM'S PUSSY – DJ BLAST 🎶🤩",
    "GITHUB IN YOUR MOM'S PUSSY – HOSTING MY BOT 👊😍",
    "YOUR SISTER'S VPS – 24/7 BASH FUCK COMMANDS 🔥",
    "I'LL CUT YOUR DICK OFF AFTER STICKING IT IN YOUR MOMMY'S PUSSY 🔪😂",
    "LISTEN – YOUR MOM'S AND SISTER'S PUSSY BOTH 👿👊",
    "SEEING YOU MAKES ME PITY YOUR RANDI SISTER 💥🔥",
    "DON'T BOUNCE TOO MUCH OR I'LL FUCK YOUR MOM IN 1 MIN ✅🤣",
    "ASK YOUR MOM WHO FUCKED HER THAT DARK NIGHT 😂😳",
    "SPOTIFY IN YOUR MOM'S PUSSY – LOFI ALL DAY 🎶😍",
    "I'LL OPEN NEW RANDI BROTHEL FOR YOUR MOM 👊🤣",
    "I'M YOUR DAD – I MAKE YOUR MOM WORK AND DRINK WITH CASH 🍷🔥",
    "I'LL SHOVE MY HUGE DICK IN YOUR SISTER'S PUSSY – SHE'LL DIE 🤩😳",
    "FULL KINGFISHER BOTTLE IN YOUR MOMMY'S PUSSY – SMASH INSIDE 😱😂",
    "I'LL FUCK YOUR MOM SO MUCH SHE'LL DREAM ABOUT IT 🥳😍",
    "I'LL CHASE AND FUCK YOUR MOM & SISTER – EVEN IF THEY SAY NO 😎🤣",
    "SELL YOUR MOMMY'S PUSSY ON OLX – OPEN BROTHEL FOR YOUR SISTER 😝😍",
    "I'LL FUCK YOUR MOM'S PUSSY SO GOOD YOU CAN'T STAY AWAY 😏🤩",
    "LEARN FROM YOUR SISTER HOW TO GET ASS FUCKED 😏🤬",
    "I'M YOUR MOM'S LOVER AND YOUR SISTER'S LOVE – COME SUCK 🤩💥",
    "PUSSYBOY", "DICK HAIR", "MOM'S PUBES", "MOTHERFUCKER", "YOUR MOM'S CUNT", "DICK BALLS",
    "YOUR SIS BIGGEST WHORE", "YOUR DAD'S A CUCK", "WE FUCKED YOUR MOM", "CATCH SPEED DICKHEAD",
    "MATCH DAD'S SPEED", "GOT FUCKED BY DAD", "I'LL RAPE YOU BITCH", "YOUR MOM GOT FUCKED",
    "SISTERFUCKER SHAME", "BASTARD", "SHAME ON YOU", "WHORE'S SON", "SUCK MY DICK",
    "GO SUCK YOUR MOM", "SON YOUR MOM BIGGEST RANDI", "MISTAKE MAKING YOU", "THOUSAND DICKS IN YOUR ASS",
    "YOUR MOM'S BLACK CUNT", "YOUR MOM RANDIIII", "MY DICK BALLS", "DOG DICK IN YOUR ASS",
    "LISTEN MOTHERFUCKER", "YOUR MOM'S PUSSY", "TAKE MY DICK IF YOU WANT", "FAGGOT", "IDIOT",
    "I'LL DRIVE JCB ON YOUR MOM'S CUNT", "YOU IDIOT FAMILY IDIOT", "I'LL WRITE ABCD IN YOUR MOM'S CUNT",
    "RANDIII", "I'LL FUCK", "RANDI'S PUP", "SEND YOUR MOM", "I'M YOUR DAD", "I'LL SELL YOUR MOM ON GB ROAD",
    "YOUR MOM CHEAP RANDI", "YOUR MOM RANDI", "HOLD MY DICK MADARCHOD", "GET OUT MADARCHOD",
    "RANDI'S KID", "YOUR SEXY SIS CUNT OPEN",
]

COLLECTION_NAME = "english_raid_targets"

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

@custom_handler(filters.all & ~filters.private, group=-18)
async def english_reply_raid_handler(c: Client, m: Message):
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

@on_message("ereplyraid", allow_stan=True)
async def activate_ereplyraid(c: Client, m: Message):
    bot_id = c.me.id
    if m.reply_to_message and m.reply_to_message.from_user:
        target_user = m.reply_to_message.from_user
    else:
        try:
            target_user = await c.get_users(m.command[1])
        except:
            return await Pbxbot.delete(m, "`Reply to a user or give username/ID.`")
    if target_user.is_self or target_user.id in Config.DEVS:
        return await Pbxbot.delete(m, "`Can't raid myself or devs.`")
    username = f"@{target_user.username}" if target_user.username else target_user.mention
    msg = await m.reply_text("`Activating English Reply Raid...`")
    if await is_raid_active(bot_id, target_user.id):
        return await msg.edit(f"`Already active on {username}`")
    await add_raid_target(bot_id, target_user.id)
    await msg.edit(f"**✅ English Reply Raid Activated on {username}**")

@on_message("dereplyraid", allow_stan=True)
async def deactivate_ereplyraid(c: Client, m: Message):
    bot_id = c.me.id
    if m.reply_to_message and m.reply_to_message.from_user:
        target_user = m.reply_to_message.from_user
    else:
        try:
            target_user = await c.get_users(m.command[1])
        except:
            return await Pbxbot.delete(m, "`Reply to a user or give username/ID.`")
    username = f"@{target_user.username}" if target_user.username else target_user.mention
    msg = await m.reply_text("`Deactivating English Reply Raid...`")
    if not await is_raid_active(bot_id, target_user.id):
        return await msg.edit(f"`No active raid on {username}`")
    await remove_raid_target(bot_id, target_user.id)
    await msg.edit(f"**❌ English Reply Raid Deactivated on {username}**")

HelpMenu("ereplyraid").add(
    "ereplyraid", "<reply/id/username>", "Start pure English reply raid.", "ereplyraid @user"
).add(
    "dereplyraid", "<reply/id/username>", "Stop English reply raid.", "dereplyraid @user"
).info("Pure English Raid – No interference with other raids!").done()
