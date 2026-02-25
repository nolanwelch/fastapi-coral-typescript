import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient) -> None:
    response = await client.post(
        "/users/", json={"name": "Alice", "email": "alice@example.com"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_list_users(client: AsyncClient) -> None:
    await client.post("/users/", json={"name": "Alice", "email": "alice@example.com"})
    await client.post("/users/", json={"name": "Bob", "email": "bob@example.com"})

    response = await client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_get_user(client: AsyncClient) -> None:
    create_resp = await client.post(
        "/users/", json={"name": "Alice", "email": "alice@example.com"}
    )
    user_id = create_resp.json()["id"]

    response = await client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Alice"


@pytest.mark.asyncio
async def test_get_user_not_found(client: AsyncClient) -> None:
    response = await client.get("/users/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_user(client: AsyncClient) -> None:
    create_resp = await client.post(
        "/users/", json={"name": "Alice", "email": "alice@example.com"}
    )
    user_id = create_resp.json()["id"]

    response = await client.patch(f"/users/{user_id}", json={"name": "Alice Updated"})
    assert response.status_code == 200
    assert response.json()["name"] == "Alice Updated"
    assert response.json()["email"] == "alice@example.com"


@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient) -> None:
    create_resp = await client.post(
        "/users/", json={"name": "Alice", "email": "alice@example.com"}
    )
    user_id = create_resp.json()["id"]

    response = await client.delete(f"/users/{user_id}")
    assert response.status_code == 204

    get_resp = await client.get(f"/users/{user_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_create_duplicate_email(client: AsyncClient) -> None:
    await client.post("/users/", json={"name": "Alice", "email": "alice@example.com"})
    response = await client.post(
        "/users/", json={"name": "Bob", "email": "alice@example.com"}
    )
    assert response.status_code == 409
