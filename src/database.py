from motor.motor_asyncio import AsyncIOMotorClient

from src.config import settings as s


class DataBase:
    client: AsyncIOMotorClient = None


mongo_db = DataBase()
mongo_url = f'mongodb://{s.MO_USER}:{s.MO_PASS}@{s.MO_HOST}:{s.MO_PORT}'


async def get_db() -> AsyncIOMotorClient:
    return mongo_db.client


async def open_mongo_db():
    mongo_db.client = AsyncIOMotorClient(str(mongo_url))
    # Creates an index for deleting a document after the date has expired
    await mongo_db.client[s.MO_DBNAME][s.secrets_collection].create_index(
        'expire_at', expireAfterSeconds=0
    )


async def close_mongo_db():
    mongo_db.client.close()
