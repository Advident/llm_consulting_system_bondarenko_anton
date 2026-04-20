import pytest


@pytest.mark.asyncio
async def test_register_login_me(client):
    # register
    response = await client.post(
        "/auth/register",
        json={
            "email": "test@email.com",
            "password": "12345678",
        },
    )
    assert response.status_code == 201

    # login
    response = await client.post(
        "/auth/login",
        data={
            "username": "test@email.com",
            "password": "12345678",
        },
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    # me
    response = await client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@email.com"