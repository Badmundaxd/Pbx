import random

from Pbxbot import __version__
from Pbxbot.core import ENV, db

# ══════════════════════════════════════════════════════
#  GROUP ALIVE TEMPLATES
# ══════════════════════════════════════════════════════

GROUP_ALIVE_TEMPLATES = [
    (
"╔══════════════════════╗\n"
"  👥 P̷B̷X̷ 4.0 — ɢʀᴏᴜᴘ ᴀʟɪᴠᴇ 👥\n"
"╚══════════════════════╝\n\n"
"┌─────────────────────┐\n"
"  🤖 sᴇssɪᴏɴ  ›  {name}\n"
"  🆔 ɪᴅ       ›  {session_id}\n"
"  ⚙️ ᴘʏʀᴏɢʀᴀᴍ ›  {pyrogram}\n"
"  🚀 ᴠᴇʀsɪᴏɴ  ›  {Pbxbot}\n"
"  🧬 ᴘʏᴛʜᴏɴ   ›  {python}\n"
"  ⏳ ᴜᴘᴛɪᴍᴇ   ›  {uptime}\n"
"└─────────────────────┘\n\n"
"🔥 [P̷B̷X̷ ᴄʜᴀᴛ](https://t.me/PBX_UPDATE) 🔥"
    ),
]


# ══════════════════════════════════════════════════════
#  GROUP PING TEMPLATES
# ══════════════════════════════════════════════════════

GROUP_PING_TEMPLATES = [
    (
"╔══════════════════════╗\n"
"   👥 P̷B̷X̷ 4.0 — ɢʀᴏᴜᴘ ⚡\n"
"╚══════════════════════╝\n\n"
"┌─────────────────────┐\n"
"  🤖 sᴇssɪᴏɴ  ›  {name}\n"
"  🆔 ɪᴅ       ›  `{session_id}`\n"
"  🏓 sᴘᴇᴇᴅ    ›  {speed} ᴍs\n"
"  ⏳ ᴜᴘᴛɪᴍᴇ   ›  {uptime}\n"
"└─────────────────────┘\n\n"
"🔥 [P̷B̷X̷ ᴄʜᴀᴛ](https://t.me/PBX_UPDATE) 🔥"
    ),
]


# ══════════════════════════════════════════════════════
#  TEMPLATE FUNCTIONS
# ══════════════════════════════════════════════════════

async def group_alive_template(name: str, session_id: int, uptime: str) -> str:
    message = random.choice(GROUP_ALIVE_TEMPLATES)
    return message.format(
        name=name,
        session_id=session_id,
        pyrogram=__version__["pyrogram"],
        Pbxbot=__version__["Pbxbot"],
        python=__version__["python"],
        uptime=uptime,
    )


async def group_ping_template(speed: float, uptime: str, name: str, session_id: int) -> str:
    message = random.choice(GROUP_PING_TEMPLATES)
    return message.format(
        speed=speed,
        uptime=uptime,
        name=name,
        session_id=session_id,
    )

# ══════════════════════════════════════════════════════
#  MUSIC ALIVE TEMPLATES
# ══════════════════════════════════════════════════════

MUSIC_ALIVE_TEMPLATES = [
    (
"╔══════════════════════╗\n"
"  🎵 P̷B̷X̷ 4.0 — ᴍᴜsɪᴄ ᴀʟɪᴠᴇ 🎵\n"
"╚══════════════════════╝\n\n"
"┌─────────────────────┐\n"
"  👑 ᴏᴡɴᴇʀ    ›  {owner}\n"
"  ⚙️ ᴘʏʀᴏɢʀᴀᴍ ›  {pyrogram}\n"
"  🚀 ᴠᴇʀsɪᴏɴ  ›  {Pbxbot}\n"
"  🧬 ᴘʏᴛʜᴏɴ   ›  {python}\n"
"  ⏳ ᴜᴘᴛɪᴍᴇ   ›  {uptime}\n"
"  🎧 sᴇssɪᴏɴ  ›  ᴍᴜsɪᴄ\n"
"└─────────────────────┘\n\n"
"🔥 [P̷B̷X̷ ᴄʜᴀᴛ](https://t.me/PBX_UPDATE) 🔥"
    ),
]


# ══════════════════════════════════════════════════════
#  MUSIC PING TEMPLATES
# ══════════════════════════════════════════════════════

MUSIC_PING_TEMPLATES = [
    """
╔══════════════════════╗
   🎵 P̷B̷X̷ 4.0 — ᴍᴜsɪᴄ ⚡
╚══════════════════════╝

┌─────────────────────┐
  🏓 sᴘᴇᴇᴅ    ›  {speed} ᴍs
  ⏳ ᴜᴘᴛɪᴍᴇ   ›  {uptime}
  👑 ᴏᴡɴᴇʀ    ›  {owner}
  🎧 sᴇssɪᴏɴ  ›  ᴍᴜsɪᴄ
└─────────────────────┘

🔥 <b><i><a href='https://t.me/PBX_UPDATE'>P̷B̷X̷ ᴄʜᴀᴛ</a></i></b> 🔥
""",
]


# ══════════════════════════════════════════════════════
#  TEMPLATE FUNCTIONS
# ══════════════════════════════════════════════════════

async def music_alive_template(owner: str, uptime: str) -> str:
    message = random.choice(MUSIC_ALIVE_TEMPLATES)
    return message.format(
        owner=owner,
        pyrogram=__version__["pyrogram"],
        Pbxbot=__version__["Pbxbot"],
        python=__version__["python"],
        uptime=uptime,
    )


async def music_ping_template(speed: float, uptime: str, owner: str) -> str:
    message = random.choice(MUSIC_PING_TEMPLATES)
    return message.format(speed=speed, uptime=uptime, owner=owner)


# ══════════════════════════════════════════════════════
#  SPAM ALIVE TEMPLATES
# ══════════════════════════════════════════════════════

SPAM_ALIVE_TEMPLATES = [
    (
"╔══════════════════════╗\n"
"   ☠️ P̷B̷X̷ 4.0 — ᴀʟɪᴠᴇ ☠️\n"
"╚══════════════════════╝\n\n"
"┌─────────────────────┐\n"
"  👑 ᴏᴡɴᴇʀ    ›  {owner}\n"
"  ⚙️ ᴘʏʀᴏɢʀᴀᴍ ›  {pyrogram}\n"
"  🚀 ᴠᴇʀsɪᴏɴ  ›  {Pbxbot}\n"
"  🧬 ᴘʏᴛʜᴏɴ   ›  {python}\n"
"  ⏳ ᴜᴘᴛɪᴍᴇ   ›  {uptime}\n"
"└─────────────────────┘\n\n"
"🔥 [P̷B̷X̷ ᴄʜᴀᴛ](https://t.me/PBX_UPDATE) 🔥"
    ),
]


# ══════════════════════════════════════════════════════
#  SPAM PING TEMPLATES
# ══════════════════════════════════════════════════════

SPAM_PING_TEMPLATES = [
    """
╔══════════════════════╗
    ⚡ P̷B̷X̷ 4.0 — ᴘɪɴɢ ⚡
╚══════════════════════╝

┌─────────────────────┐
  🏓 sᴘᴇᴇᴅ    ›  {speed} ᴍs
  ⏳ ᴜᴘᴛɪᴍᴇ   ›  {uptime}
  👑 ᴏᴡɴᴇʀ    ›  {owner}
  🤖 sᴇssɪᴏɴ  ›  sᴘᴀᴍ
└─────────────────────┘

🔥 <b><i><a href='https://t.me/PBX_UPDATE'>P̷B̷X̷ ᴄʜᴀᴛ</a></i></b> 🔥
""",
]


# ══════════════════════════════════════════════════════
#  TEMPLATE FUNCTIONS
# ══════════════════════════════════════════════════════

async def spam_alive_template(owner: str, uptime: str) -> str:
    template = await db.get_env(ENV.alive_template)
    if template:
        message = template
    else:
        message = random.choice(SPAM_ALIVE_TEMPLATES)
    return message.format(
        owner=owner,
        pyrogram=__version__["pyrogram"],
        Pbxbot=__version__["Pbxbot"],
        python=__version__["python"],
        uptime=uptime,
    )


async def spam_ping_template(speed: float, uptime: str, owner: str) -> str:
    message = random.choice(SPAM_PING_TEMPLATES)
    return message.format(speed=speed, uptime=uptime, owner=owner)

ALIVE_TEMPLATES = [
    (
"╭━━━━━━━━━━━━━━━━╮\n"
"┃  ✦ ☠️ P̷B̷X̷ 4.0 ᴀʟɪᴠᴇ ☠️ ✦  ┃\n"
"╰━━━━━━━━━━━━━━━━╯\n\n"
"┏━━━━━━━━━━━━━━━━━┓\n"
"┃ 👑 ᴏᴡɴᴇʀ › {owner}\n"
"┃ ⚙️ ᴘʏʀᴏɢʀᴀᴍ › {pyrogram}\n"
"┃ 🚀 ᴘʙxʙᴏᴛ › {Pbxbot}\n"
"┃ 🧬 ᴘʏᴛʜᴏɴ › {python}\n"
"┃ ⏳ ᴜᴘᴛɪᴍᴇ › {uptime}\n"
"┗━━━━━━━━━━━━━━━━━┛\n\n"
"  ╔══════════════╗\n"
"     🔥 [ᴘʙx ᴄʜᴀᴛ](https://t.me/PBX_UPDATE) 🔥\n"
"  ╚══════════════╝\n"
        ),
]

PING_TEMPLATES = [
    """
╔══════════════════════╗
    ⚡ P̷B̷X̷ 4.0 — ᴘɪɴɢ ⚡
╚══════════════════════╝

┌─────────────────────┐
  🏓 sᴘᴇᴇᴅ   ›  {speed} ᴍs
  ⏳ ᴜᴘᴛɪᴍᴇ  ›  {uptime}
  👑 ᴏᴡɴᴇʀ   ›  {owner}
└─────────────────────┘

🔥 <b><i><a href='https://t.me/PBX_UPDATE'>P̷B̷X̷ ᴄʜᴀᴛ</a></i></b> 🔥
""",
]

HELP_MENU_TEMPLATES = [
    """**☠️ ʜᴇʟᴘ ᴍᴇɴᴜ ғᴏʀ:** {owner}

__📦 ʟᴏᴀᴅᴇᴅ__ **{plugins} ᴘʟᴜɢɪɴs** __ᴡɪᴛʜ ᴀ ᴛᴏᴛᴀʟ ᴏғ__ **{commands} ᴄᴏᴍᴍᴀɴᴅs.**

**📖 ᴘᴀɢᴇ:** __{current}/{last}__"""
]

COMMAND_MENU_TEMPLATES = [
    """**📁 ᴘʟᴜɢɪɴ ғɪʟᴇ:** `{file}`
**🧬 ᴘʟᴜɢɪɴ ɪɴғᴏ:** __{info}__

**📜 ʟᴏᴀᴅᴇᴅ ᴄᴏᴍᴍᴀɴᴅs:** `{commands}`"""
]

ANIME_TEMPLATES = [
    """
{name}

╭━━━━━━━━━━━━━━━━━╮
│ ⭐ sᴄᴏʀᴇ › `{score}`
│ 📚 sᴏᴜʀᴄᴇ › `{source}`
│ 🎬 ᴛʏᴘᴇ › `{mtype}`
│ 📺 ᴇᴘɪsᴏᴅᴇs › `{episodes}`
│ ⏱️ ᴅᴜʀᴀᴛɪᴏɴ › `{duration} minutes`
│ 📊 sᴛᴀᴛᴜs › `{status}`
│ 🎞️ ғᴏʀᴍᴀᴛ › `{format}`
│ 🎭 ɢᴇɴʀᴇ › `{genre}`
│ 🏷️ ᴛᴀɢs › `{tags}`
│ 🔞 ᴀᴅᴜʟᴛ ʀᴀᴛᴇᴅ › `{isAdult}`
│ 🎨 sᴛᴜᴅɪᴏ › `{studio}`
│ 🎥 ᴛʀᴀɪʟᴇʀ › {trailer}
│ 🌐 ᴡᴇʙsɪᴛᴇ › {siteurl}
│ 📝 sʏɴᴏᴘsɪs › [ᴄʟɪᴄᴋ ʜᴇʀᴇ]({description})
╰━━━━━━━━━━━━━━━━━╯
"""
]

MANGA_TEMPLATES = [
    """
{name}

╭━━━━━━━━━━━━━━━━━╮
│ ⭐ sᴄᴏʀᴇ › `{score}`
│ 📚 sᴏᴜʀᴄᴇ › `{source}`
│ 📖 ᴛʏᴘᴇ › `{mtype}`
│ 📄 ᴄʜᴀᴘᴛᴇʀs › `{chapters}`
│ 📚 ᴠᴏʟᴜᴍᴇs › `{volumes}`
│ 📊 sᴛᴀᴛᴜs › `{status}`
│ 🎞️ ғᴏʀᴍᴀᴛ › `{format}`
│ 🎭 ɢᴇɴʀᴇ › `{genre}`
│ 🔞 ᴀᴅᴜʟᴛ ʀᴀᴛᴇᴅ › `{isAdult}`
│ 🌐 ᴡᴇʙsɪᴛᴇ › {siteurl}
│ 📝 sʏɴᴏᴘsɪs › [ᴄʟɪᴄᴋ ʜᴇʀᴇ]({description})
╰━━━━━━━━━━━━━━━━━╯
"""
]

CHARACTER_TEMPLATES = [
    """
{name}

╭━━━━━━━━━━━━━━━━━╮
│ 👤 ɢᴇɴᴅᴇʀ › `{gender}`
│ 🎂 ʙɪʀᴛʜᴅᴀʏ › `{date_of_birth}`
│ 🔢 ᴀɢᴇ › `{age}`
│ 💉 ʙʟᴏᴏᴅ ᴛʏᴘᴇ › `{blood_type}`
│ ❤️ ғᴀᴠᴏᴜʀɪᴛᴇs › `{favorites}`
│ 🌐 ᴡᴇʙsɪᴛᴇ › {siteurl}{role_in}
╰━━━━━━━━━━━━━━━━━╯
{description}
"""
]

AIRING_TEMPLATES = [
    """
{name}

╭━━━━━━━━━━━━━━━━━╮
│ 📊 sᴛᴀᴛᴜs › `{status}`
│ 📺 ᴇᴘɪsᴏᴅᴇ › `{episode}`
╰━━━━━━━━━━━━━━━━━╯{airing_info}
"""
]

ANILIST_USER_TEMPLATES = [
    """
**✨ {name}**

╭━━━ ᴀɴɪᴍᴇ ━━━╮
│ 📊 ᴄᴏᴜɴᴛ › `{anime_count}`
│ ⭐ sᴄᴏʀᴇ › `{anime_score}`
│ ⏰ ᴍɪɴᴜᴛᴇs › `{minutes}`
│ 📺 ᴇᴘɪsᴏᴅᴇs › `{episodes}`
╰━━━━━━━━━━━━━━━╯
╭━━━ ᴍᴀɴɢᴀ ━━━╮
│ 📊 ᴄᴏᴜɴᴛ › `{manga_count}`
│ ⭐ sᴄᴏʀᴇ › `{manga_score}`
│ 📄 ᴄʜᴀᴘᴛᴇʀs › `{chapters}`
│ 📚 ᴠᴏʟᴜᴍᴇs › `{volumes}`
╰━━━━━━━━━━━━━━━╯

🌐 ᴡᴇʙsɪᴛᴇ: {siteurl}
"""
]

CLIMATE_TEMPLATES = [
    """
🌆 {city_name}, {country}

╭━━━━━━━━━━━━━━━━━╮
│ 🌤️ ᴡᴇᴀᴛʜᴇʀ › {weather}
│ 🕐 ᴛɪᴍᴇᴢᴏɴᴇ › {timezone}
│ 🌅 sᴜɴʀɪsᴇ › {sunrise}
│ 🌇 sᴜɴsᴇᴛ › {sunset}
│ 💨 ᴡɪɴᴅ › {wind}
│ 🌡️ ᴛᴇᴍᴘᴇʀᴀᴛᴜʀᴇ › {temperature}°C
│ 🤔 ғᴇᴇʟs ʟɪᴋᴇ › {feels_like}°C
│ ❄️ ᴍɪɴɪᴍᴜᴍ › {temp_min}°C
│ 🔥 ᴍᴀxɪᴍᴜᴍ › {temp_max}°C
│ 📊 ᴘʀᴇssᴜʀᴇ › {pressure} hPa
│ 💧 ʜᴜᴍɪᴅɪᴛʏ › {humidity}%
│ 👁️ ᴠɪsɪʙɪʟɪᴛʏ › {visibility} m
│ ☁️ ᴄʟᴏᴜᴅs › {clouds}%
╰━━━━━━━━━━━━━━━━━╯
"""
]

AIR_POLLUTION_TEMPLATES = [
    """
🌆 {city_name}

╭━━━━━━━━━━━━━━━━━╮
│ 📊 ᴀQɪ › {aqi}
│ 💨 ᴄᴀʀʙᴏɴ ᴍᴏɴᴏxɪᴅᴇ › {co}
│ 🌫️ ɴɪᴛʀᴏɢᴇɴ ᴍᴏɴᴏxɪᴅᴇ › {no}
│ 🌫️ ɴɪᴛʀᴏɢᴇɴ ᴅɪᴏxɪᴅᴇ › {no2}
│ 💨 ᴏᴢᴏɴᴇ › {o3}
│ 🌫️ sᴜʟᴘʜᴜʀ ᴅɪᴏxɪᴅᴇ › {so2}
│ 💨 ᴀᴍᴍᴏɴɪᴀ › {nh3}
│ 🔬 ᴘᴍ{sub2_5} › {pm2_5}
│ 🔬 ᴘᴍ{sub10} › {pm10}
╰━━━━━━━━━━━━━━━━━╯
"""
]

GITHUB_USER_TEMPLATES = [
    """
✨ {username} ({git_id})

╭━━━ {id_type} ━━━╮
│ 👤 ɴᴀᴍᴇ › [{name}]({profile_url})
│ 📝 ʙʟᴏɢ › {blog}
│ 🏢 ᴄᴏᴍᴘᴀɴʏ › {company}
│ 📧 ᴇᴍᴀɪʟ › {email}
│ 📍 ʟᴏᴄᴀᴛɪᴏɴ › {location}
│ 📦 ʀᴇᴘᴏs › {public_repos}
│ 📄 ɢɪsᴛs › {public_gists}
│ 👥 ғᴏʟʟᴏᴡᴇʀs › {followers}
│ 👤 ғᴏʟʟᴏᴡɪɴɢ › {following}
│ 📅 ᴄʀᴇᴀᴛᴇᴅ › {created_at}
╰━━━━━━━━━━━━━━━╯

**💫 ʙɪᴏ:** {bio}
"""
]

STATISTICS_TEMPLATES = [
    """
✨ {name}

╭━━━ ᴄʜᴀɴɴᴇʟs ━━━╮
│ 📊 ᴛᴏᴛᴀʟ › `{channels}`
│ 👮 ᴀᴅᴍɪɴ › `{ch_admin}`
│ 👑 ᴏᴡɴᴇʀ › `{ch_owner}`
╰━━━━━━━━━━━━━━━╯

╭━━━ ɢʀᴏᴜᴘs ━━━╮
│ 📊 ᴛᴏᴛᴀʟ › `{groups}`
│ 👮 ᴀᴅᴍɪɴ › `{gc_admin}`
│ 👑 ᴏᴡɴᴇʀ › `{gc_owner}`
╰━━━━━━━━━━━━━━━╯

╭━━━ ᴏᴛʜᴇʀs ━━━╮
│ 👤 ᴘʀɪᴠᴀᴛᴇ › `{users}`
│ 🤖 ʙᴏᴛs › `{bots}`
│ 💬 ᴜɴʀᴇᴀᴅ ᴍsɢ › `{unread_msg}`
│ 🔔 ᴜɴʀᴇᴀᴅ ᴍᴇɴᴛɪᴏɴs › `{unread_mention}`
╰━━━━━━━━━━━━━━━╯

⏰ **ᴛɪᴍᴇ ᴛᴀᴋᴇɴ:** `{time_taken}`
"""
]

GWARN_TEMPLATES = [
    """
╭━━━ ⚠️ ɢ-ᴡᴀʀɴ ━━━╮
│ 🎯 ᴠɪᴄᴛɪᴍ › {name}
│ ⚠️ ᴡᴀʀɴs › {warn_count}/{warn_limit}
│ 📝 ʀᴇᴀsᴏɴ › {reason}
╰━━━━━━━━━━━━━━━╯
"""
]

GWARN_AUTOBAN_TEMPLATES = [
    """
╭━━━ 🔨 ᴀᴜᴛᴏ-ɢʙᴀɴ (ᴡᴀʀɴ ʟɪᴍɪᴛ) ━━━╮
│ 🎯 ᴠɪᴄᴛɪᴍ › {name}
│ ⚠️ ᴡᴀʀɴs › {warn_limit}/{warn_limit}
│ ✅ sᴜᴄᴄᴇss › {success}
│ ❌ ғᴀɪʟᴇᴅ › {failed}
│ 📝 ʀᴇᴀsᴏɴ › Auto-GBan: Warn limit reached
╰━━━━━━━━━━━━━━━╯
"""
]

GTEMPBAN_TEMPLATES = [
    """
╭━━━ ⏳ ɢ-ᴛᴇᴍᴘʙᴀɴ ━━━╮
│ 🎯 ᴠɪᴄᴛɪᴍ › {name}
│ ⏰ ᴅᴜʀᴀᴛɪᴏɴ › {duration}
│ ✅ sᴜᴄᴄᴇss › {success}
│ ❌ ғᴀɪʟᴇᴅ › {failed}
│ 📝 ʀᴇᴀsᴏɴ › {reason}
╰━━━━━━━━━━━━━━━╯
"""
]

GPIN_TEMPLATES = [
    """
╭━━━ 📌 ɢ-ᴘɪɴ ━━━╮
│ ✅ ᴘɪɴɴᴇᴅ ɪɴ › {success} ᴄʜᴀᴛs
│ ❌ ғᴀɪʟᴇᴅ › {failed} ᴄʜᴀᴛs
╰━━━━━━━━━━━━━━━╯
"""
]

GBROADCAST_TEMPLATES = [
    """
╭━━━ 📢 ɢ-ʙʀᴏᴀᴅᴄᴀsᴛ ━━━╮
│ ✅ sᴇɴᴛ › {success}
│ ❌ ғᴀɪʟᴇᴅ › {failed}
│ 📊 ᴛᴏᴛᴀʟ › {total}
│ ⏱️ ᴛɪᴍᴇ › {time_taken}
╰━━━━━━━━━━━━━━━╯
"""
]

GCHECK_TEMPLATES = [
    """
╭━━━ 🔍 ɢ-ᴄʜᴇᴄᴋ ━━━╮
│ 👤 ᴜsᴇʀ › {mention}
│ 🆔 ɪᴅ › `{user_id}`
│ 🔨 ɢʙᴀɴ › {gban_status}
│ 🔇 ɢᴍᴜᴛᴇ › {gmute_status}
│ ⚠️ ɢᴡᴀʀɴ › {gwarn_status}
│ 👻 sʜᴀᴅᴏᴡʙᴀɴ › {shadow_status}
│ 🔕 sɪʟᴇɴᴄᴇᴅ › {silence_status}
│ 💳 ᴄʀᴇᴅɪᴛs › `{credits}`
│ 👑 ʀᴏʟᴇ › {role}
╰━━━━━━━━━━━━━━━╯
"""
]

GSTATS_TEMPLATES = [
    """
╭━━━ 📊 ɢ-sᴛᴀᴛs ━━━╮
│ 💬 ɢʀᴏᴜᴘs › `{groups}`
│ 📢 ᴄʜᴀɴɴᴇʟs › `{channels}`
│ 🔨 ɢʙᴀɴs › `{gbans}`
│ 🔇 ɢᴍᴜᴛᴇs › `{gmutes}`
│ ⚠️ ɢᴡᴀʀɴs › `{gwarns}`
│ 👻 sʜᴀᴅᴏᴡʙᴀɴs › `{gshadowbans}`
│ 🔕 sɪʟᴇɴᴄᴇᴅ › `{gsilenced}`
│ 🚫 ɢʙʟᴀᴄᴋʟɪsᴛ ᴡᴏʀᴅs › `{gblacklists}`
│ 📊 ᴛᴏᴛᴀʟ ᴅɪᴀʟᴏɢs › `{total}`
╰━━━━━━━━━━━━━━━╯
"""
]

GSHADOWBAN_TEMPLATES = [
    """
╭━━━ 👻 ɢ-sʜᴀᴅᴏᴡʙᴀɴ ━━━╮
│ 🎯 ᴠɪᴄᴛɪᴍ › {name}
│ ✅ sᴜᴄᴄᴇss › {success}
│ ❌ ғᴀɪʟᴇᴅ › {failed}
│ 📝 ʀᴇᴀsᴏɴ › {reason}
╰━━━━━━━━━━━━━━━╯
"""
]

GSILENCE_TEMPLATES = [
    """
╭━━━ 🔕 ɢ-sɪʟᴇɴᴄᴇ ━━━╮
│ 🎯 ᴠɪᴄᴛɪᴍ › {name}
│ ✅ sᴜᴄᴄᴇss › {success}
│ ❌ ғᴀɪʟᴇᴅ › {failed}
│ 📝 ʀᴇᴀsᴏɴ › {reason}
╰━━━━━━━━━━━━━━━╯
"""
]

GUNSILENCE_TEMPLATES = [
    """
╭━━━ 🔔 ɢ-ᴜɴsɪʟᴇɴᴄᴇ ━━━╮
│ 🎯 ᴜsᴇʀ › {name}
│ ✅ sᴜᴄᴄᴇss › {success}
│ ❌ ғᴀɪʟᴇᴅ › {failed}
╰━━━━━━━━━━━━━━━╯
"""
]

GBLACKLIST_TEMPLATES = [
    """
╭━━━ 🚫 ɢ-ʙʟᴀᴄᴋʟɪsᴛ ━━━╮
│ 🔤 ᴡᴏʀᴅ › `{word}`
│ ✅ ᴀᴄᴛɪᴠᴇ ɪɴ › {groups} ɢʀᴏᴜᴘs
╰━━━━━━━━━━━━━━━╯
"""
]

GBAN_TEMPLATES = [
    """
╭━━━ {gtype} ━━━╮
│ 🎯 ᴠɪᴄᴛɪᴍ › {name}
│ ✅ sᴜᴄᴄᴇss › {success}
│ ❌ ғᴀɪʟᴇᴅ › {failed}
│ 📝 ʀᴇᴀsᴏɴ › {reason}
╰━━━━━━━━━━━━━━━╯
"""
]

USAGE_TEMPLATES = [
    """
**📊 ᴅɪsᴋ & ᴅʏɴᴏ ᴜsᴀɢᴇ:**

**➜ ᴅʏɴᴏ ᴜsᴀɢᴇ ғᴏʀ** `{appName}`
    ◈ __{appHours}ʜʀs {appMinutes}ᴍɪɴs__ | __{appPercentage}%__

**➜ ᴅʏɴᴏ ʀᴇᴍᴀɪɴɪɴɢ ᴛʜɪs ᴍᴏɴᴛʜ:**
    ◈ __{hours}ʜʀs {minutes}ᴍɪɴs__ | __{percentage}%__

**➜ ᴅɪsᴋ ᴜsᴀɢᴇ:**
    ◈ __{diskUsed}ɢʙ__ / __{diskTotal}ɢʙ__ | __{diskPercent}%__

**➜ ᴍᴇᴍᴏʀʏ ᴜsᴀɢᴇ:**
    ◈ __{memoryUsed}ɢʙ__ / __{memoryTotal}ɢʙ__ | __{memoryPercent}%__
"""
]

USER_INFO_TEMPLATES = [
    """
**✨ ᴜsᴇʀ ɪɴғᴏ ᴏғ {mention}:**

**➜ ғɪʀsᴛ ɴᴀᴍᴇ:** `{firstName}`
**➜ ʟᴀsᴛ ɴᴀᴍᴇ:** `{lastName}`
**➜ ᴜsᴇʀ ɪᴅ:** `{userId}`

**➜ ᴄᴏᴍᴍᴏɴ ɢʀᴏᴜᴘs:** `{commonGroups}`
**➜ ᴅᴄ ɪᴅ:** `{dcId}`
**➜ ᴘɪᴄᴛᴜʀᴇs:** `{totalPictures}`
**➜ ʀᴇsᴛʀɪᴄᴛᴇᴅ:** `{isRestricted}`
**➜ ᴠᴇʀɪғɪᴇᴅ:** `{isVerified}`
**➜ ʙᴏᴛ:** `{isBot}`
**➜ ʙɪᴏ:** `{bio}`

**🔥 ᴘᴏᴡᴇʀᴇᴅ ʙʏ P̷B̷X̷ 4.0**
"""
]

CHAT_INFO_TEMPLATES = [
    """
**✨ ᴄʜᴀᴛ ɪɴғᴏ:**

**➜ ᴄʜᴀᴛ ɴᴀᴍᴇ:** `{chatName}`
**➜ ᴄʜᴀᴛ ɪᴅ:** `{chatId}`
**➜ ᴄʜᴀᴛ ʟɪɴᴋ:** {chatLink}
**➜ ᴏᴡɴᴇʀ:** {chatOwner}
**➜ ᴅᴄ ɪᴅ:** `{dcId}`
**➜ ᴍᴇᴍʙᴇʀs:** `{membersCount}`
**➜ ᴀᴅᴍɪɴs:** `{adminsCount}`
**➜ ʙᴏᴛs:** `{botsCount}`
**➜ ᴅᴇsᴄʀɪᴘᴛɪᴏɴ:** `{description}`

**🔥 ᴘᴏᴡᴇʀᴇᴅ ʙʏ P̷B̷X̷ 4.0**
"""
]


async def alive_template(owner: str, uptime: str) -> str:
    template = await db.get_env(ENV.alive_template)
    if template:
        message = template
    else:
        message = random.choice(ALIVE_TEMPLATES)
    return message.format(
        owner=owner,
        pyrogram=__version__["pyrogram"],
        Pbxbot=__version__["Pbxbot"],
        python=__version__["python"],
        uptime=uptime,
    )


async def ping_template(speed: float, uptime: str, owner: str) -> str:
    template = await db.get_env(ENV.ping_template)
    if template:
        message = template
    else:
        message = random.choice(PING_TEMPLATES)
    return message.format(speed=speed, uptime=uptime, owner=owner)


async def help_template(
    owner: str, cmd_n_plgn: tuple[int, int], page: tuple[int, int]
) -> str:
    template = await db.get_env(ENV.help_template)
    if template:
        message = template
    else:
        message = random.choice(HELP_MENU_TEMPLATES)
    return message.format(
        owner=owner,
        commands=cmd_n_plgn[0],
        plugins=cmd_n_plgn[1],
        current=page[0],
        last=page[1],
    )


async def command_template(file: str, info: str, commands: str) -> str:
    template = await db.get_env(ENV.command_template)
    if template:
        message = template
    else:
        message = random.choice(COMMAND_MENU_TEMPLATES)
    return message.format(file=file, info=info, commands=commands)


async def anime_template(**kwargs) -> str:
    template = await db.get_env(ENV.anime_template)
    if template:
        message = template
    else:
        message = random.choice(ANIME_TEMPLATES)
    return message.format(**kwargs)


async def manga_templates(**kwargs) -> str:
    template = await db.get_env(ENV.manga_template)
    if template:
        message = template
    else:
        message = random.choice(MANGA_TEMPLATES)
    return message.format(**kwargs)


async def character_templates(**kwargs) -> str:
    template = await db.get_env(ENV.character_template)
    if template:
        message = template
    else:
        message = random.choice(CHARACTER_TEMPLATES)
    return message.format(**kwargs)


async def airing_templates(**kwargs) -> str:
    template = await db.get_env(ENV.airing_template)
    if template:
        message = template
    else:
        message = random.choice(AIRING_TEMPLATES)
    return message.format(**kwargs)


async def anilist_user_templates(
    name: str, anime: tuple, manga: tuple, siteurl: str
) -> str:
    template = await db.get_env(ENV.anilist_user_template)
    if template:
        message = template
    else:
        message = random.choice(ANILIST_USER_TEMPLATES)
    return message.format(
        name=name,
        anime_count=anime[0],
        anime_score=anime[1],
        minutes=anime[2],
        episodes=anime[3],
        manga_count=manga[0],
        manga_score=manga[1],
        chapters=manga[2],
        volumes=manga[3],
        siteurl=siteurl,
    )


async def climate_templates(**kwargs) -> str:
    template = await db.get_env(ENV.climate_template)
    if template:
        message = template
    else:
        message = random.choice(CLIMATE_TEMPLATES)
    return message.format(**kwargs)


async def airpollution_templates(**kwargs) -> str:
    template = await db.get_env(ENV.airpollution_template)
    if template:
        message = template
    else:
        message = random.choice(AIR_POLLUTION_TEMPLATES)
    return message.format(**kwargs)


async def statistics_templates(**kwargs) -> str:
    template = await db.get_env(ENV.statistics_template)
    if template:
        message = template
    else:
        message = random.choice(STATISTICS_TEMPLATES)
    return message.format(**kwargs)


async def github_user_templates(**kwargs) -> str:
    template = await db.get_env(ENV.github_user_template)
    if template:
        message = template
    else:
        message = random.choice(GITHUB_USER_TEMPLATES)
    return message.format(**kwargs)


async def gban_templates(**kwargs) -> str:
    template = await db.get_env(ENV.gban_template)
    if template:
        message = template
    else:
        message = random.choice(GBAN_TEMPLATES)
    return message.format(**kwargs)


async def usage_templates(**kwargs) -> str:
    template = await db.get_env(ENV.usage_template)
    if template:
        message = template
    else:
        message = random.choice(USAGE_TEMPLATES)
    return message.format(**kwargs)


async def user_info_templates(**kwargs) -> str:
    template = await db.get_env(ENV.user_info_template)
    if template:
        message = template
    else:
        message = random.choice(USER_INFO_TEMPLATES)
    return message.format(**kwargs)


async def chat_info_templates(**kwargs) -> str:
    template = await db.get_env(ENV.chat_info_template)
    if template:
        message = template
    else:
        message = random.choice(CHAT_INFO_TEMPLATES)
    return message.format(**kwargs)
    


async def gwarn_templates(**kwargs) -> str:
    message = random.choice(GWARN_TEMPLATES)
    return message.format(**kwargs)


async def gwarn_autoban_templates(**kwargs) -> str:
    message = random.choice(GWARN_AUTOBAN_TEMPLATES)
    return message.format(**kwargs)


async def gtempban_templates(**kwargs) -> str:
    message = random.choice(GTEMPBAN_TEMPLATES)
    return message.format(**kwargs)


async def gpin_templates(**kwargs) -> str:
    message = random.choice(GPIN_TEMPLATES)
    return message.format(**kwargs)


async def gbroadcast_templates(**kwargs) -> str:
    message = random.choice(GBROADCAST_TEMPLATES)
    return message.format(**kwargs)


async def gcheck_templates(**kwargs) -> str:
    message = random.choice(GCHECK_TEMPLATES)
    return message.format(**kwargs)


async def gstats_templates(**kwargs) -> str:
    message = random.choice(GSTATS_TEMPLATES)
    return message.format(**kwargs)


async def gshadowban_templates(**kwargs) -> str:
    message = random.choice(GSHADOWBAN_TEMPLATES)
    return message.format(**kwargs)


async def gsilence_templates(**kwargs) -> str:
    message = random.choice(GSILENCE_TEMPLATES)
    return message.format(**kwargs)


async def gunsilence_templates(**kwargs) -> str:
    message = random.choice(GUNSILENCE_TEMPLATES)
    return message.format(**kwargs)


async def gblacklist_templates(**kwargs) -> str:
    message = random.choice(GBLACKLIST_TEMPLATES)
    return message.format(**kwargs)
