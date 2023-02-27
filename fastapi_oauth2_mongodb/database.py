from motor.motor_asyncio import AsyncIOMotorClient

asyncio_motor_client = AsyncIOMotorClient("mongodb://localhost:27017/")
falra_db = asyncio_motor_client["falra_db"]
users_collection = falra_db["users"]
logs_collection = falra_db["logs"]
