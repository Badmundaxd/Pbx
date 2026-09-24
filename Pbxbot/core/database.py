import datetime
import time
import uuid
from motor import motor_asyncio
from motor.core import AgnosticClient
from .config import Config, Symbols
from .logger import LOGS


class Database:
    def __init__(self, uri: str) -> None:
        self.client: AgnosticClient = motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self.client["Pbxbot"]

        # ================= COLLECTIONS =================
        self.afk            = self.db["afk"]
        self.antiflood      = self.db["antiflood"]
        self.autopost       = self.db["autopost"]
        self.blacklist      = self.db["blacklist"]
        self.echo           = self.db["echo"]
        self.env            = self.db["env"]
        self.filter         = self.db["filter"]
        self.forcesub       = self.db["forcesub"]
        self.gachabots      = self.db["gachabots"]
        self.gban           = self.db["gban"]
        self.gmute          = self.db["gmute"]
        self.greetings      = self.db["greetings"]
        self.mute           = self.db["mute"]
        self.pmpermit       = self.db["pmpermit"]
        self.pmoff          = self.db["pmoff"]
        self.session        = self.db["session"]
        self.snips          = self.db["snips"]
        self.stan_users     = self.db["stan_users"]
        self.states_col     = self.db["user_states"]
        self.supersudos     = self.db["supersudos"]
        self.special        = self.db["special"]
        self.blocked_numbers = self.db["blocked_numbers"]
        self.tokens         = self.db["tokens"]
        self.users          = self.db["users"]
        self.bad_users      = self.db["bad_users"]
        self.english_raid_targets = self.db["english_raid_targets"]
        self.hindi_raid_targets   = self.db["hindi_raid_targets"]
        self.mixed_raid_targets   = self.db["mixed_raid_targets"]
        self.punjabi_raid_targets = self.db["punjabi_raid_targets"]
        self.custom_raid    = self.db["custom_raid"]
        # ── Global Superpower Systems ─────────────────
        self.gwarn          = self.db["gwarn"]
        self.gshadowban     = self.db["gshadowban"]
        self.gsilence       = self.db["gsilence"]
        self.gblacklist     = self.db["gblacklist"]

    # ══════════════════════════════════════════════════
    #  CONNECTION
    # ══════════════════════════════════════════════════

    async def connect(self):
        try:
            await self.client.admin.command("ping")
            LOGS.info(
                f"{Symbols.bullet * 3} Database Connection Established! {Symbols.bullet * 3}"
            )
        except Exception as e:
            LOGS.info(f"{Symbols.cross_mark} DatabaseErr: {e} ")
            quit(1)

    def get_datetime(self) -> str:
        return datetime.datetime.now().strftime("%d/%m/%Y - %H:%M")

    # ══════════════════════════════════════════════════
    #  ENV
    # ══════════════════════════════════════════════════

    async def set_env(self, name: str, value: str) -> None:
        await self.env.update_one(
            {"name": name}, {"$set": {"value": value}}, upsert=True
        )

    async def get_env(self, name: str) -> str | None:
        data = await self.env.find_one({"name": name})
        return data["value"] if data else None

    async def rm_env(self, name: str) -> None:
        await self.env.delete_one({"name": name})

    async def is_env(self, name: str) -> bool:
        return bool(await self.env.find_one({"name": name}))

    async def get_all_env(self) -> list:
        return [i async for i in self.env.find({})]

    # ══════════════════════════════════════════════════
    #  STAN USERS
    # ══════════════════════════════════════════════════

    async def is_stan(self, client: int, user_id: int) -> bool:
        return bool(await self.stan_users.find_one({"client": client, "user_id": user_id}))

    async def add_stan(self, client: int, user_id: int) -> bool:
        if await self.is_stan(client, user_id):
            return False
        await self.stan_users.insert_one(
            {"client": client, "user_id": user_id, "date": self.get_datetime()}
        )
        return True

    async def rm_stan(self, client: int, user_id: int) -> bool:
        if not await self.is_stan(client, user_id):
            return False
        await self.stan_users.delete_one({"client": client, "user_id": user_id})
        return True

    async def get_stans(self, client: int) -> list:
        return [i async for i in self.stan_users.find({"client": client})]

    async def get_all_stans(self) -> list:
        return [i async for i in self.stan_users.find({})]

    # ══════════════════════════════════════════════════
    #  SESSIONS (basic userbot)
    # ══════════════════════════════════════════════════

    async def is_session(self, user_id: int) -> bool:
        return bool(await self.session.find_one({"user_id": user_id}))

    async def update_session(self, user_id: int, session: str) -> None:
        await self.session.update_one(
            {"user_id": user_id},
            {"$set": {"session": session, "date": self.get_datetime()}},
            upsert=True,
        )
        await self.tokens.delete_many({"user_id": user_id})

    async def rm_session(self, user_id: int) -> None:
        await self.session.delete_one({"user_id": user_id})

    async def get_session(self, user_id: int):
        return await self.session.find_one({"user_id": user_id})

    async def get_all_sessions(self) -> list:
        return [i async for i in self.session.find({})]

    async def get_user_session_count(self, user_id: int) -> int:
        sessions = await self.get_all_sessions()
        return sum(1 for s in sessions if s["user_id"] == user_id)

    # ══════════════════════════════════════════════════
    #  TOKENS
    # ══════════════════════════════════════════════════

    async def generate_token(self, user_id: int) -> tuple[str, float]:
        token = str(uuid.uuid4())[:22]
        expiry = time.time() + 300
        await self.tokens.insert_one({
            "user_id": user_id,
            "token": token,
            "expiry": expiry,
            "used": False
        })
        return token, expiry

    async def validate_token(self, token: str, user_id: int) -> bool:
        token_data = await self.tokens.find_one({"token": token, "user_id": user_id})
        if not token_data or token_data["used"]:
            return False
        if time.time() > token_data["expiry"]:
            await self.tokens.delete_one({"token": token})
            return False
        return True

    async def mark_token_used(self, token: str) -> None:
        await self.tokens.update_one({"token": token}, {"$set": {"used": True}})

    async def get_user_token_count(self, user_id: int) -> int:
        return await self.tokens.count_documents({"user_id": user_id})

    # ══════════════════════════════════════════════════
    #  USER STATES
    # ══════════════════════════════════════════════════

    async def set_user_state(self, user_id, state):
        await self.states_col.update_one(
            {"user_id": user_id}, {"$set": {"state": state}}, upsert=True
        )

    async def get_user_state(self, user_id):
        doc = await self.states_col.find_one({"user_id": user_id})
        return doc.get("state") if doc else None

    async def reset_user_state(self, user_id: int) -> None:
        await self.states_col.delete_one({"user_id": user_id})

    async def reset_all_states(self):
        await self.states_col.delete_many({})

    # ══════════════════════════════════════════════════
    #  GBAN (per-session)
    # ══════════════════════════════════════════════════

    async def is_gbanned(self, user_id: int, owner_id: int) -> bool:
        return bool(await self.gban.find_one({"user_id": user_id, "owner_id": owner_id}))

    async def add_gban(self, user_id: int, reason: str, owner_id: int) -> bool:
        if await self.is_gbanned(user_id, owner_id):
            return False
        await self.gban.insert_one({
            "user_id":  user_id,
            "owner_id": owner_id,
            "reason":   reason,
            "date":     self.get_datetime()
        })
        return True

    async def rm_gban(self, user_id: int, owner_id: int):
        doc = await self.gban.find_one({"user_id": user_id, "owner_id": owner_id})
        if not doc:
            return None
        await self.gban.delete_one({"user_id": user_id, "owner_id": owner_id})
        return doc["reason"]

    async def get_gban(self, owner_id: int = None) -> list:
        if owner_id is None:
            return [i async for i in self.gban.find({})]
        return [i async for i in self.gban.find({"owner_id": owner_id})]

    async def get_gban_user(self, user_id: int, owner_id: int) -> dict | None:
        return await self.gban.find_one({"user_id": user_id, "owner_id": owner_id})

    # ══════════════════════════════════════════════════
    #  GMUTE (per-session)
    # ══════════════════════════════════════════════════

    async def is_gmuted(self, user_id: int, owner_id: int) -> bool:
        return bool(await self.gmute.find_one({"user_id": user_id, "owner_id": owner_id}))

    async def add_gmute(self, user_id: int, reason: str, owner_id: int) -> bool:
        if await self.is_gmuted(user_id, owner_id):
            return False
        await self.gmute.insert_one({
            "user_id":  user_id,
            "owner_id": owner_id,
            "reason":   reason,
            "date":     self.get_datetime()
        })
        return True

    async def rm_gmute(self, user_id: int, owner_id: int):
        doc = await self.gmute.find_one({"user_id": user_id, "owner_id": owner_id})
        if not doc:
            return None
        await self.gmute.delete_one({"user_id": user_id, "owner_id": owner_id})
        return doc["reason"]

    async def get_gmute(self, owner_id: int = None) -> list:
        if owner_id is None:
            return [i async for i in self.gmute.find({})]
        return [i async for i in self.gmute.find({"owner_id": owner_id})]

    # ══════════════════════════════════════════════════
    #  GWARN (per-session)
    # ══════════════════════════════════════════════════

    GWARN_LIMIT = 3

    async def add_gwarn(self, user_id: int, reason: str, owner_id: int) -> int:
        await self.gwarn.update_one(
            {"user_id": user_id, "owner_id": owner_id},
            {
                "$push": {"warns": {"reason": reason, "date": self.get_datetime()}},
                "$inc":  {"count": 1},
                "$setOnInsert": {"user_id": user_id, "owner_id": owner_id},
            },
            upsert=True,
        )
        data = await self.gwarn.find_one({"user_id": user_id, "owner_id": owner_id})
        return data["count"]

    async def rm_gwarn(self, user_id: int, owner_id: int) -> int:
        data = await self.gwarn.find_one({"user_id": user_id, "owner_id": owner_id})
        count = data["count"] if data else 0
        await self.gwarn.delete_one({"user_id": user_id, "owner_id": owner_id})
        return count

    async def get_gwarn(self, user_id: int, owner_id: int) -> dict | None:
        return await self.gwarn.find_one({"user_id": user_id, "owner_id": owner_id})

    async def get_gwarn_count(self, user_id: int, owner_id: int) -> int:
        data = await self.gwarn.find_one({"user_id": user_id, "owner_id": owner_id})
        return data["count"] if data else 0

    async def is_gwarned(self, user_id: int, owner_id: int) -> bool:
        return bool(await self.gwarn.find_one({"user_id": user_id, "owner_id": owner_id}))

    async def get_all_gwarns(self, owner_id: int = None) -> list:
        if owner_id is None:
            return [i async for i in self.gwarn.find({})]
        return [i async for i in self.gwarn.find({"owner_id": owner_id})]

    # ══════════════════════════════════════════════════
    #  GSHADOWBAN
    # ══════════════════════════════════════════════════

    async def add_gshadowban(self, owner_id: int, user_id: int, reason: str) -> bool:
        if await self.is_gshadowbanned(owner_id, user_id):
            return False
        await self.gshadowban.insert_one(
            {"owner_id": owner_id, "user_id": user_id, "reason": reason, "date": self.get_datetime()}
        )
        return True

    async def rm_gshadowban(self, owner_id: int, user_id: int):
        if not await self.is_gshadowbanned(owner_id, user_id):
            return None
        data = await self.gshadowban.find_one({"owner_id": owner_id, "user_id": user_id})
        reason = data["reason"]
        await self.gshadowban.delete_one({"owner_id": owner_id, "user_id": user_id})
        return reason

    async def is_gshadowbanned(self, owner_id: int, user_id: int) -> bool:
        return bool(await self.gshadowban.find_one({"owner_id": owner_id, "user_id": user_id}))

    async def get_all_gshadowbans(self, owner_id: int) -> list:
        return [i async for i in self.gshadowban.find({"owner_id": owner_id})]

    # ══════════════════════════════════════════════════
    #  GSILENCE
    # ══════════════════════════════════════════════════

    async def add_gsilence(self, owner_id: int, user_id: int, reason: str) -> bool:
        if await self.is_gsilenced(owner_id, user_id):
            return False
        await self.gsilence.insert_one(
            {"owner_id": owner_id, "user_id": user_id, "reason": reason, "date": self.get_datetime()}
        )
        return True

    async def rm_gsilence(self, owner_id: int, user_id: int):
        if not await self.is_gsilenced(owner_id, user_id):
            return None
        data = await self.gsilence.find_one({"owner_id": owner_id, "user_id": user_id})
        reason = data["reason"]
        await self.gsilence.delete_one({"owner_id": owner_id, "user_id": user_id})
        return reason

    async def is_gsilenced(self, owner_id: int, user_id: int) -> bool:
        return bool(await self.gsilence.find_one({"owner_id": owner_id, "user_id": user_id}))

    async def get_all_gsilenced(self, owner_id: int) -> list:
        return [i async for i in self.gsilence.find({"owner_id": owner_id})]

    # ══════════════════════════════════════════════════
    #  GBLACKLIST
    # ══════════════════════════════════════════════════

    async def add_gblacklist(self, word: str) -> bool:
        if await self.is_gblacklisted(word):
            return False
        await self.gblacklist.insert_one({"word": word.lower(), "date": self.get_datetime()})
        return True

    async def rm_gblacklist(self, word: str) -> bool:
        if not await self.is_gblacklisted(word):
            return False
        await self.gblacklist.delete_one({"word": word.lower()})
        return True

    async def is_gblacklisted(self, word: str) -> bool:
        return bool(await self.gblacklist.find_one({"word": word.lower()}))

    async def get_all_gblacklists(self) -> list:
        return [i async for i in self.gblacklist.find({})]

    # ══════════════════════════════════════════════════
    #  MUTE
    # ══════════════════════════════════════════════════

    async def add_mute(self, client: int, user_id: int, chat_id: int, reason: str):
        await self.mute.update_one(
            {"client": client, "user_id": user_id, "chat_id": chat_id},
            {"$set": {"reason": reason, "date": self.get_datetime()}},
            upsert=True,
        )

    async def rm_mute(self, client: int, user_id: int, chat_id: int) -> str:
        doc = await self.mute.find_one({"client": client, "user_id": user_id, "chat_id": chat_id})
        reason = doc["reason"] if doc else ""
        await self.mute.delete_one({"client": client, "user_id": user_id, "chat_id": chat_id})
        return reason

    async def is_muted(self, client: int, user_id: int, chat_id: int) -> bool:
        return bool(await self.mute.find_one({"client": client, "user_id": user_id, "chat_id": chat_id}))

    async def get_mute(self, client: int, user_id: int, chat_id: int):
        return await self.mute.find_one({"client": client, "user_id": user_id, "chat_id": chat_id})

    # ══════════════════════════════════════════════════
    #  AFK
    # ══════════════════════════════════════════════════

    async def set_afk(self, user_id: int, reason: str, media: int, media_type: str) -> None:
        await self.afk.update_one(
            {"user_id": user_id},
            {"$set": {"reason": reason, "time": time.time(), "media": media, "media_type": media_type}},
            upsert=True,
        )

    async def get_afk(self, user_id: int):
        return await self.afk.find_one({"user_id": user_id})

    async def is_afk(self, user_id: int) -> bool:
        return bool(await self.afk.find_one({"user_id": user_id}))

    async def rm_afk(self, user_id: int) -> None:
        await self.afk.delete_one({"user_id": user_id})

    # ══════════════════════════════════════════════════
    #  ANTIFLOOD
    # ══════════════════════════════════════════════════

    async def set_flood(self, client_chat: tuple[int, int], settings: dict):
        await self.antiflood.update_one(
            {"client": client_chat[0], "chat": client_chat[1]},
            {"$set": settings},
            upsert=True,
        )

    async def get_flood(self, client_chat: tuple[int, int]):
        data = await self.antiflood.find_one({"client": client_chat[0], "chat": client_chat[1]})
        return data or {}

    async def is_flood(self, client_chat: tuple[int, int]) -> bool:
        data = await self.get_flood(client_chat)
        return bool(data) and data.get("limit", 0) != 0

    async def get_all_floods(self) -> list:
        return [i async for i in self.antiflood.find({})]

    # ══════════════════════════════════════════════════
    #  AUTOPOST
    # ══════════════════════════════════════════════════

    async def set_autopost(self, client: int, from_channel: int, to_channel: int):
        await self.autopost.update_one(
            {"client": client},
            {"$push": {"autopost": {"from_channel": from_channel, "to_channel": to_channel, "date": self.get_datetime()}}},
            upsert=True,
        )

    async def get_autopost(self, client: int, from_channel: int):
        return await self.autopost.find_one(
            {"client": client, "autopost": {"$elemMatch": {"from_channel": from_channel}}}
        )

    async def is_autopost(self, client: int, from_channel: int, to_channel: int = None) -> bool:
        if to_channel:
            data = await self.autopost.find_one(
                {"client": client, "autopost": {"$elemMatch": {"from_channel": from_channel, "to_channel": to_channel}}}
            )
        else:
            data = await self.autopost.find_one(
                {"client": client, "autopost": {"$elemMatch": {"from_channel": from_channel}}}
            )
        return bool(data)

    async def rm_autopost(self, client: int, from_channel: int, to_channel: int):
        await self.autopost.update_one(
            {"client": client},
            {"$pull": {"autopost": {"from_channel": from_channel, "to_channel": to_channel}}},
        )

    async def get_all_autoposts(self, client: int) -> list:
        return [i async for i in self.autopost.find({"client": client})]

    # ══════════════════════════════════════════════════
    #  BLACKLIST
    # ══════════════════════════════════════════════════

    async def add_blacklist(self, client: int, chat: int, blacklist: str):
        await self.blacklist.update_one(
            {"client": client, "chat": chat},
            {"$push": {"blacklist": blacklist}},
            upsert=True,
        )

    async def rm_blacklist(self, client: int, chat: int, blacklist: str):
        await self.blacklist.update_one(
            {"client": client, "chat": chat},
            {"$pull": {"blacklist": blacklist}},
        )

    async def is_blacklist(self, client: int, chat: int, blacklist: str) -> bool:
        return blacklist in await self.get_all_blacklists(client, chat)

    async def get_all_blacklists(self, client: int, chat: int) -> list:
        data = await self.blacklist.find_one({"client": client, "chat": chat})
        return data["blacklist"] if data else []

    async def get_blacklist_clients(self) -> list:
        return [i async for i in self.blacklist.find({})]

    # ══════════════════════════════════════════════════
    #  ECHO
    # ══════════════════════════════════════════════════

    async def set_echo(self, client: int, chat: int, user: int):
        await self.echo.update_one(
            {"client": client, "chat": chat},
            {"$push": {"echo": user}},
            upsert=True,
        )

    async def rm_echo(self, client: int, chat: int, user: int):
        await self.echo.update_one(
            {"client": client, "chat": chat},
            {"$pull": {"echo": user}},
        )

    async def is_echo(self, client: int, chat: int, user: int) -> bool:
        return user in await self.get_all_echo(client, chat)

    async def get_all_echo(self, client: int, chat: int) -> list:
        data = await self.echo.find_one({"client": client, "chat": chat})
        return data["echo"] if data else []

    # ══════════════════════════════════════════════════
    #  FILTERS
    # ══════════════════════════════════════════════════

    async def set_filter(self, client: int, chat: int, keyword: str, msgid: int):
        await self.filter.update_one(
            {"client": client, "chat": chat},
            {"$push": {"filter": {"keyword": keyword, "msgid": msgid}}},
            upsert=True,
        )

    async def rm_filter(self, client: int, chat: int, keyword: str):
        await self.filter.update_one(
            {"client": client, "chat": chat},
            {"$pull": {"filter": {"keyword": keyword}}},
        )

    async def rm_all_filters(self, client: int, chat: int):
        await self.filter.delete_one({"client": client, "chat": chat})

    async def is_filter(self, client: int, chat: int, keyword: str) -> bool:
        return bool(await self.get_filter(client, chat, keyword))

    async def get_filter(self, client: int, chat: int, keyword: str):
        return await self.filter.find_one(
            {"client": client, "chat": chat, "filter": {"$elemMatch": {"keyword": keyword}}}
        )

    async def get_all_filters(self, client: int, chat: int) -> list:
        data = await self.filter.find_one({"client": client, "chat": chat})
        return data["filter"] if data else []

    # ══════════════════════════════════════════════════
    #  SNIPS
    # ══════════════════════════════════════════════════

    async def set_snip(self, client: int, chat: int, keyword: str, msgid: int):
        await self.snips.update_one(
            {"client": client, "chat": chat},
            {"$push": {"snips": {"keyword": keyword, "msgid": msgid}}},
            upsert=True,
        )

    async def rm_snip(self, client: int, chat: int, keyword: str):
        await self.snips.update_one(
            {"client": client, "chat": chat},
            {"$pull": {"snips": {"keyword": keyword}}},
        )

    async def rm_all_snips(self, client: int, chat: int):
        await self.snips.delete_one({"client": client, "chat": chat})

    async def is_snip(self, client: int, chat: int, keyword: str) -> bool:
        return bool(await self.get_snip(client, chat, keyword))

    async def get_snip(self, client: int, chat: int, keyword: str):
        return await self.snips.find_one(
            {"client": client, "chat": chat, "snips": {"$elemMatch": {"keyword": keyword}}}
        )

    async def get_all_snips(self, client: int, chat: int) -> list:
        data = await self.snips.find_one({"client": client, "chat": chat})
        return data["snips"] if data else []
        
    # ══════════════════════════════════════════════════
    #  BLOCK NUMBER 
    # ══════════════════════════════════════════════════
    
        
    async def block_number(self, phone_number: str):
        await self.blocked_numbers.update_one(
            {"phone_number": phone_number},
            {"$set": {"blocked": True}},
            upsert=True,
        )

    async def unblock_number(self, phone_number: str):
        await self.blocked_numbers.delete_one({"phone_number": phone_number})

    async def is_number_blocked(self, phone_number: str) -> bool:
        doc = await self.blocked_numbers.find_one({"phone_number": phone_number})
        return bool(doc and doc.get("blocked", False))

    async def get_all_blocked_numbers(self):
        return [i async for i in self.blocked_numbers.find({})]
        

    # ══════════════════════════════════════════════════
    #  PMPERMIT
    # ══════════════════════════════════════════════════

    async def add_pmpermit(self, client: int, user: int):
        await self.pmpermit.update_one(
            {"client": client, "user": user},
            {"$set": {"date": self.get_datetime()}},
            upsert=True,
        )

    async def rm_pmpermit(self, client: int, user: int):
        await self.pmpermit.delete_one({"client": client, "user": user})

    async def is_pmpermit(self, client: int, user: int) -> bool:
        return bool(await self.pmpermit.find_one({"client": client, "user": user}))

    async def get_pmpermit(self, client: int, user: int):
        return await self.pmpermit.find_one({"client": client, "user": user})

    async def get_all_pmpermits(self, client: int) -> list:
        return [i async for i in self.pmpermit.find({"client": client})]

    async def set_pmoff(self, client: int, value: bool) -> None:
        await self.pmoff.update_one(
            {"client": client},
            {"$set": {"client": client, "disabled": value}},
            upsert=True,
        )

    async def is_pmoff(self, client: int) -> bool:
        doc = await self.pmoff.find_one({"client": client})
        return bool(doc and doc.get("disabled", False))

    # ══════════════════════════════════════════════════
    #  GREETINGS (welcome / goodbye)
    # ══════════════════════════════════════════════════

    async def set_welcome(self, client: int, chat: int, message: int):
        await self.greetings.update_one(
            {"client": client, "chat": chat, "welcome": True},
            {"$set": {"message": message}},
            upsert=True,
        )

    async def rm_welcome(self, client: int, chat: int):
        await self.greetings.delete_one({"client": client, "chat": chat, "welcome": True})

    async def is_welcome(self, client: int, chat: int) -> bool:
        return bool(await self.greetings.find_one({"client": client, "chat": chat, "welcome": True}))

    async def get_welcome(self, client: int, chat: int):
        return await self.greetings.find_one({"client": client, "chat": chat, "welcome": True})

    async def set_goodbye(self, client: int, chat: int, message: int):
        await self.greetings.update_one(
            {"client": client, "chat": chat, "welcome": False},
            {"$set": {"message": message}},
            upsert=True,
        )

    async def rm_goodbye(self, client: int, chat: int):
        await self.greetings.delete_one({"client": client, "chat": chat, "welcome": False})

    async def is_goodbye(self, client: int, chat: int) -> bool:
        return bool(await self.greetings.find_one({"client": client, "chat": chat, "welcome": False}))

    async def get_goodbye(self, client: int, chat: int):
        return await self.greetings.find_one({"client": client, "chat": chat, "welcome": False})

    async def get_all_greetings(self, client: int) -> list:
        return [i async for i in self.greetings.find({"client": client})]

    # ══════════════════════════════════════════════════
    #  FORCESUB
    # ══════════════════════════════════════════════════

    async def add_forcesub(self, chat: int, must_join: int):
        await self.forcesub.update_one(
            {"chat": chat}, {"$push": {"must_join": must_join}}, upsert=True
        )

    async def rm_forcesub(self, chat: int, must_join: int) -> int:
        await self.forcesub.update_one(
            {"chat": chat}, {"$pull": {"must_join": must_join}}
        )
        data = await self.forcesub.find_one({"chat": chat})
        return len(data["must_join"]) if data else 0

    async def rm_all_forcesub(self, in_chat: int):
        await self.forcesub.delete_one({"chat": in_chat})

    async def is_forcesub(self, chat: int, must_join: int) -> bool:
        data = await self.forcesub.find_one({"chat": chat})
        return bool(data and must_join in data["must_join"])

    async def get_forcesub(self, in_chat: int):
        return await self.forcesub.find_one({"chat": in_chat})

    async def get_all_forcesubs(self) -> list:
        return [i async for i in self.forcesub.find({})]

    # ══════════════════════════════════════════════════
    #  GACHABOTS
    # ══════════════════════════════════════════════════

    async def add_gachabot(self, client: int, bot: tuple[int, str], catch_command: str, chat_id: int):
        await self.gachabots.update_one(
            {"client": client, "bot": bot[0]},
            {"$set": {"username": bot[1], "catch_command": catch_command, "chat_id": chat_id, "date": self.get_datetime()}},
            upsert=True,
        )

    async def rm_gachabot(self, client: int, bot: int, chat_id: int = None):
        if chat_id:
            await self.gachabots.delete_one({"client": client, "bot": bot, "chat_id": chat_id})
        else:
            await self.gachabots.delete_one({"client": client, "bot": bot})

    async def is_gachabot(self, client: int, bot: int, chat_id: int) -> bool:
        return bool(await self.gachabots.find_one({"client": client, "bot": bot, "chat_id": chat_id}))

    async def get_gachabot(self, client: int, bot: int, chat_id: int):
        return await self.gachabots.find_one({"client": client, "bot": bot, "chat_id": chat_id})

    async def get_all_gachabots(self, client: int) -> list:
        return [i async for i in self.gachabots.find({"client": client})]

    async def get_all_gachabots_id(self) -> list:
        return await self.gachabots.distinct("bot")

    # ══════════════════════════════════════════════════
    #  OTP
    # ══════════════════════════════════════════════════

    async def update_last_otp(self, user_id, otp):
        await self.session.update_one(
            {"user_id": user_id}, {"$set": {"last_otp": otp}}, upsert=True
        )

    async def get_last_otp(self, user_id):
        doc = await self.session.find_one({"user_id": user_id})
        return doc.get("last_otp") if doc else None

    # ══════════════════════════════════════════════════
    #  BAD USERS
    # ══════════════════════════════════════════════════

    async def get_all_Bad_users(self) -> list:
        return await self.bad_users.find({}).to_list(length=None)

    async def is_Bad_user(self, user_id: int) -> bool:
        return bool(await self.bad_users.find_one({"user_id": user_id}))

    async def add_Bad_user(self, user_id: int) -> None:
        await self.bad_users.update_one(
            {"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True
        )

    async def rm_Bad_user(self, user_id: int) -> None:
        await self.bad_users.delete_one({"user_id": user_id})

    # ══════════════════════════════════════════════════
    #  SUPERSUDO
    # ══════════════════════════════════════════════════

    async def add_supersudo(self, user_id: int) -> None:
        await self.supersudos.update_one(
            {"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True
        )

    async def rm_supersudo(self, user_id: int) -> None:
        await self.supersudos.delete_one({"user_id": user_id})

    async def is_supersudo(self, user_id: int) -> bool:
        return bool(await self.supersudos.find_one({"user_id": user_id}))

    async def get_all_supersudos(self) -> list:
        return await self.supersudos.find({}).to_list(length=None)

    # ══════════════════════════════════════════════════
    #  SPECIAL PROTECTED IDs
    # ══════════════════════════════════════════════════

    async def get_all_specials(self):
        return await self.special.find({}).to_list(length=None)

    async def add_special_user(self, user_id: int):
        await self.special.update_one(
            {"type": "user", "user_id": user_id},
            {"$set": {"user_id": user_id, "type": "user"}},
            upsert=True
        )

    async def add_special_group(self, group_id: int):
        await self.special.update_one(
            {"type": "group", "group_id": group_id},
            {"$set": {"group_id": group_id, "type": "group"}},
            upsert=True
        )

    async def rm_special_user(self, user_id: int):
        await self.special.delete_one({"type": "user", "user_id": user_id})

    async def rm_special_group(self, group_id: int):
        await self.special.delete_one({"type": "group", "group_id": group_id})

    async def is_special_user(self, user_id: int) -> bool:
        return bool(await self.special.find_one({"type": "user", "user_id": user_id}))

    async def is_special_group(self, group_id: int) -> bool:
        return bool(await self.special.find_one({"type": "group", "group_id": group_id}))

    # ══════════════════════════════════════════════════
    #  CREDIT SYSTEM
    # ══════════════════════════════════════════════════

    async def get_user(self, user_id: int):
        user = await self.users.find_one({"user_id": user_id})
        if not user:
            user = {
                "user_id": user_id,
                "credits": 0,
                "referred_by": None,
                "referred_users": [],
                "sessions_added": 0,
                "created_at": datetime.datetime.now()
            }
            await self.users.insert_one(user)
        return user

    async def add_credits(self, user_id: int, amount: int):
        await self.users.update_one(
            {"user_id": user_id}, {"$inc": {"credits": amount}}, upsert=True
        )

    async def deduct_credits(self, user_id: int, amount: int = 1):
        user = await self.get_user(user_id)
        if user["credits"] >= amount:
            await self.users.update_one({"user_id": user_id}, {"$inc": {"credits": -amount}})
            return True
        return False

    async def get_credits(self, user_id: int):
        user = await self.get_user(user_id)
        return user.get("credits", 0)

    async def set_referrer(self, user_id: int, referrer_id: int):
        user = await self.get_user(user_id)
        if user.get("referred_by") is None and user_id != referrer_id:
            await self.users.update_one(
                {"user_id": user_id}, {"$set": {"referred_by": referrer_id}}
            )
            await self.users.update_one(
                {"user_id": referrer_id},
                {"$addToSet": {"referred_users": user_id}, "$inc": {"credits": 1}},
                upsert=True
            )
            return True
        return False

    async def increment_sessions(self, user_id: int):
        await self.users.update_one(
            {"user_id": user_id}, {"$inc": {"sessions_added": 1}}, upsert=True
        )

    async def is_auth_user(self, user_id: int) -> bool:
        return user_id == Config.OWNER_ID

    # ══════════════════════════════════════════════════
    #  GENERIC DOC HELPERS
    # ══════════════════════════════════════════════════

    async def get_doc(self, collection: str, doc_id):
        return await self.db[collection].find_one({"_id": doc_id})

    async def set_doc(self, collection: str, doc_id, data: dict):
        await self.db[collection].replace_one({"_id": doc_id}, data, upsert=True)

    async def update_doc(self, collection: str, doc_id, update_data: dict):
        await self.db[collection].update_one({"_id": doc_id}, {"$set": update_data}, upsert=True)

    # ══════════════════════════════════════════════════
    #  CUSTOM RAID
    # ══════════════════════════════════════════════════

    async def get_custom_raid(self, user_id: int) -> list:
        doc = await self.custom_raid.find_one({"user_id": user_id})
        return doc["messages"] if doc else []

    async def add_custom_raid_msg(self, user_id: int, msg: str) -> int:
        doc = await self.custom_raid.find_one({"user_id": user_id})
        messages = (doc["messages"] if doc else []) + [msg]
        await self.custom_raid.update_one(
            {"user_id": user_id}, {"$set": {"messages": messages}}, upsert=True
        )
        return len(messages)

    async def rm_custom_raid_msg(self, user_id: int, index: int) -> bool:
        doc = await self.custom_raid.find_one({"user_id": user_id})
        if not doc or index < 1 or index > len(doc["messages"]):
            return False
        messages = doc["messages"]
        messages.pop(index - 1)
        await self.custom_raid.update_one({"user_id": user_id}, {"$set": {"messages": messages}})
        return True

    async def clear_custom_raid(self, user_id: int) -> None:
        await self.custom_raid.delete_one({"user_id": user_id})

    # ══════════════════════════════════════════════════
    #  CLEAN ALL
    # ══════════════════════════════════════════════════

    async def clean_all(self):
        collections = [
            self.session, self.gban, self.gmute, self.gwarn,
            self.gshadowban, self.gsilence, self.gblacklist, self.mute,
            self.blacklist, self.echo, self.filter, self.snips,
            self.pmpermit, self.greetings, self.forcesub, self.gachabots,
            self.env, self.antiflood, self.autopost,
            self.afk, self.stan_users, self.states_col, self.tokens,
            self.custom_raid,
        ]
        for col in collections:
            await col.delete_many({})


db = Database(Config.DATABASE_URL)
