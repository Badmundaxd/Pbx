from pymongo import MongoClient

class Database:
    def __init__(self):
        self.client = MongoClient("mongodb+srv://aujla:aujla@teji.yqkrgos.mongodb.net/")
        self.db = self.client["pbxbot"]
        self.sessions = self.db["sessions"]
        self.blocked_numbers = self.db["blocked_numbers"]

    async def update_session(self, user_id, session_string):
        self.sessions.update_one(
            {"user_id": user_id},
            {"$set": {"session_string": session_string}},
            upsert=True
        )

    async def is_number_blocked(self, phone_number):
        return bool(self.blocked_numbers.find_one({"phone_number": phone_number}))

# Instantiate
db = Database()
