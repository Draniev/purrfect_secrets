from motor.motor_asyncio import AsyncIOMotorClient

from src.config import settings as s


mongo_url = f'mongodb://{s.MO_USER}:{s.MO_PASS}@{s.MO_HOST}:{s.MO_PORT}'
mongo_client = AsyncIOMotorClient(mongo_url)

# Connects to a database or creates a new one if one does not exist.
db = mongo_client.secrets_db
