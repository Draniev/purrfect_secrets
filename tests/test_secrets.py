import asyncio
import pytest


@pytest.mark.asyncio
async def test_create_secret(client):
    secret_data = {
        "secret_body": "A very secret message",
        "secret_pass": "example",
        "lifetime": 60,
    }
    response = await client.post("/generate", json=secret_data)
    assert response.status_code == 201
    assert "secret_key" in response.json()


@pytest.mark.asyncio
async def test_get_secret(client):
    secret_data = {
        "secret_body": "A very secret message",
        "secret_pass": "example",
        "lifetime": 60,
    }
    response = await client.post("/generate", json=secret_data)
    secret_key = response.json()["secret_key"]
    secret_pass = "example"
    response = await client.get(
        f"/secrets/{secret_key}", params={"secret_pass": secret_pass}
    )
    assert response.status_code == 200
    assert "secret_body" in response.json()


@pytest.mark.asyncio
async def test_create_and_get_secret_without_pass(client):
    secret_data = {"secret_body": "A very secret message", "lifetime": 60}
    response = await client.post("/generate", json=secret_data)
    secret_key = response.json()["secret_key"]
    assert response.status_code == 201
    response = await client.get(f"/secrets/{secret_key}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_secret_wrong_pass(client):
    secret_data = {
        "secret_body": "A very secret message",
        "secret_pass": "example",
        "lifetime": 60,
    }
    response = await client.post("/generate", json=secret_data)
    secret_key = response.json()["secret_key"]
    wrong_pass = "wrong"
    assert response.status_code == 201
    response = await client.get(f"/secrets/{secret_key}")
    assert response.status_code == 403
    response = await client.get(
        f"/secrets/{secret_key}", params={"secret_pass": wrong_pass}
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_secret_deletion_after_access(client):
    secret_data = {
        "secret_body": "A very secret message",
        "secret_pass": "example",
        "lifetime": 3600,
    }
    response = await client.post("/generate", json=secret_data)
    secret_key = response.json()["secret_key"]
    secret_pass = "example"
    response = await client.get(
        f"/secrets/{secret_key}", params={"secret_pass": secret_pass}
    )
    assert response.status_code == 200
    second_response = await client.get(
        f"/secrets/{secret_key}", params={"secret_pass": secret_pass}
    )
    assert second_response.status_code == 404


@pytest.mark.asyncio
async def test_secret_expiration(client):
    secret_data = {
        "secret_body": "A very secret message",
        "secret_pass": "example",
        "lifetime": 5,
    }
    response = await client.post("/generate", json=secret_data)
    assert response.status_code == 201
    secret_key = response.json()["secret_key"]
    secret_pass = "example"
    # Wait 90 seconds to ensure the secret has expired
    await asyncio.sleep(70)
    response = await client.get(
        f"/secrets/{secret_key}", params={"secret_pass": secret_pass}
    )
    assert response.status_code == 404
