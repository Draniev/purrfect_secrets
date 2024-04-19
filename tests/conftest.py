import pytest
import pytest_asyncio
from httpx import AsyncClient

from src.config import settings as s
from src.database import open_mongo_db, close_mongo_db
from src.main import app

# Override settings for testing
s.MO_DBNAME = 'test_db'


@pytest_asyncio.fixture()
async def client():
    await open_mongo_db()
    async with AsyncClient(
        app=app, base_url="http://testserver"
    ) as test_client:
        yield test_client
        await test_client.aclose()
    await close_mongo_db()


# @pytest.fixture()
# async def client():
#     with TestClient(
#         app=app, base_url="http://testserver"
#     ) as test_client:
#         yield test_client
#         test_client.close()
