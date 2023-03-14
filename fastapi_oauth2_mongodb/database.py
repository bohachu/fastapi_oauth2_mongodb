from motor.motor_asyncio import AsyncIOMotorClient

asyncio_motor_client = AsyncIOMotorClient("mongodb://localhost:27017/")
db = asyncio_motor_client["falra_db"]
logs_collection = db["logs"]
