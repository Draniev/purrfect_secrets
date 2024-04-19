import pytest
from httpx import AsyncClient

from src.main import app


@pytest.mark.asyncio
async def test_create_secret(client):
    # async with AsyncClient(app=app, base_url="http://testserver") as client:
    secret_data = {
        "secret_body": "A very secret message",
        "secret_pass": "example",
        "lifetime": 60
    }
    response = await client.post("/generate", json=secret_data)
    assert response.status_code == 200
    assert 'secret_key' in response.json()


@pytest.mark.asyncio
async def test_get_secret():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        secret_data = {
            "secret_body": "A very secret message",
            "secret_pass": "example",
            "lifetime": 60
        }
        response = await client.post("/generate", json=secret_data)
        secret_key = response.json()['secret_key']
        secret_pass = 'example'
        response = await client.get(f"/secrets/{secret_key}", params={"secret_pass": secret_pass})
        assert response.status_code == 200
        assert 'secret_body' in response.json()


# @pytest.mark.asyncio
# async def test_create_secret(client):
#     secret_data = {
#         "secret_body": "A very secret message",
#         "secret_pass": "example",
#         "lifetime": 60
#     }
#     response = await client.post("/generate", json=secret_data)
#     assert response.status_code == 200
#     assert 'secret_key' in response.json()


# @pytest.mark.asyncio
# async def test_get_secret(client):
#     secret_data = {
#         "secret_body": "A very secret message",
#         "secret_pass": "example",
#         "lifetime": 60
#     }
#     response = await client.post("/generate", json=secret_data)
#     secret_key = response.json()['secret_key']
#     secret_pass = 'example'
#     response = await client.get(
#         f"/secrets/{secret_key}",
#         params={"secret_pass": secret_pass}
#     )
#     assert response.status_code == 200
#     assert 'secret_body' in response.json()
#

# @pytest.mark.asyncio
# async def test_get_secret_without_pass():
#     secret_key = 'existing_key'
#     async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
#         response = await ac.get(f"/secrets/{secret_key}")
#         assert response.status_code == 404
#
# @pytest.mark.asyncio
# async def test_get_secret_wrong_pass():
#     secret_key = 'existing_key'
#     wrong_secret_pass = 'wrong_pass'
#     async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
#         response = await ac.get(f"/secrets/{secret_key}", params={"secret_pass": wrong_secret_pass})
#         assert response.status_code == 403
#
# @pytest.mark.asyncio
# async def test_secret_expiration():
#     secret_data = {
#         "secret_body": "Temporary secret",
#         "secret_pass": "example",
#         "lifetime": 5  # 5 seconds
#     }
#     async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
#         create_response = await ac.post("/generate", json=secret_data)
#         assert create_response.status_code == 200
#         secret_key = create_response.json()['secret_key']
#         # Wait 90 seconds to ensure the secret has expired
#         await asyncio.sleep(90)
#         check_response = await ac.get(f"/secrets/{secret_key}")
#         assert check_response.status_code == 404
#
# @pytest.mark.asyncio
# async def test_secret_deletion_after_access():
#     # Assuming secret_key is retrieved from a test setup or previous test creation
#     secret_key = 'existing_key_to_be_accessed'
#     secret_pass = 'valid_pass'
#     async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
#         response = await ac.get(f"/secrets/{secret_key}", params={"secret_pass": secret_pass})
#         assert response.status_code == 200
#         # Check if secret is deleted
#         second_response = await ac.get(f"/secrets/{secret_key}", params={"secret_pass": secret_pass})
#         assert second_response.status_code == 404
#
