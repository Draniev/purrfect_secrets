import pytest
import pytest_asyncio
from httpx import AsyncClient

from src.config import settings as s
from src.main import app

# Override settings for testing
# s.Config.env_file = '.env.test'
s.MO_DBNAME = 'test_db'


@pytest_asyncio.fixture()
async def client():
    async with AsyncClient(
        app=app, base_url="http://testserver"
    ) as test_client:
        yield test_client
        await test_client.aclose()
