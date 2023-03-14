from database import db
from pymongo import IndexModel, ASCENDING


async def create_db_indexes():
    user_indexes = [IndexModel([("email", ASCENDING)])]
    await db.user.create_indexes(user_indexes)
    api_key_indexes = [IndexModel([("email", ASCENDING)])]
    await db.apikey.create_indexes(api_key_indexes)
