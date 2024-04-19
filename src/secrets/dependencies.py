from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Depends

from src.database import get_db
from src.secrets.services import SecretsCRUD


async def secrets_crud(conn: AsyncIOMotorClient = Depends(get_db)):
    return SecretsCRUD(conn=conn)
