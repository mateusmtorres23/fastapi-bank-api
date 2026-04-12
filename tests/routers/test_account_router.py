import pytest
from httpx import AsyncClient
from fastapi import status

@pytest.mark.asyncio
async def test_get_my_accounts(async_client: AsyncClient):
    reg_payload = {"username": "account_router_user", "password": "secure_password"}
    await async_client.post("/auth/register", json=reg_payload)
    
    login_data = {"username": "account_router_user", "password": "secure_password"}
    login_response = await async_client.post("/auth/login", data=login_data)
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}

    response = await async_client.get("/accounts/me", headers=headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["username"] == "account_router_user"
    assert "accounts" in data
    assert len(data["accounts"]) == 1
    
    account = data["accounts"][0]
    assert account["sequence_number"] == 1
    assert account["balance"] == "0.00"
    assert "account_number" not in account