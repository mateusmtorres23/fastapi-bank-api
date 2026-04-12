import pytest
from httpx import AsyncClient
from fastapi import status

async def register_and_login(client: AsyncClient, username: str) -> dict:
    await client.post("/auth/register", json={"username": username, "password": "password123"})
    login_response = await client.post("/auth/login", data={"username": username, "password": "password123"})
    token = login_response.json()["access_token"]
    
    me_response = await client.get("/accounts/me", headers={"Authorization": f"Bearer {token}"})
    user_id = me_response.json()["id"]
    
    return {"token": token, "user_id": user_id, "headers": {"Authorization": f"Bearer {token}"}}


@pytest.mark.asyncio
async def test_full_transaction_flow(async_client: AsyncClient):
    alice = await register_and_login(async_client, "alice_router")
    bob = await register_and_login(async_client, "bob_router")

    deposit_payload = {
        "user_id": alice["user_id"],
        "account_sequence_number": 1,
        "amount": 1000.00,
        "type": "deposit"
    }
    dep_response = await async_client.post(
        "/transactions/deposit", 
        json=deposit_payload, 
        headers=alice["headers"]
    )
    assert dep_response.status_code == status.HTTP_201_CREATED

    withdraw_payload = {
        "user_id": alice["user_id"],
        "account_sequence_number": 1,
        "amount": 200.00,
        "type": "withdrawal"
    }
    with_response = await async_client.post(
        "/transactions/withdraw", 
        json=withdraw_payload, 
        headers=alice["headers"]
    )
    assert with_response.status_code == status.HTTP_201_CREATED

    transfer_payload = {
        "amount": 300.00,
        "source_sequence_number": 1,
        "destination_user_id": bob["user_id"],
        "destination_sequence_number": 1
    }
    trans_response = await async_client.post(
        "/transactions/transfer", 
        json=transfer_payload, 
        headers=alice["headers"]
    )
    assert trans_response.status_code == status.HTTP_200_OK

    alice_acc_response = await async_client.get("/accounts/me", headers=alice["headers"])
    alice_balance = alice_acc_response.json()["accounts"][0]["balance"]
    assert alice_balance == "500.00"

    bob_acc_response = await async_client.get("/accounts/me", headers=bob["headers"])
    bob_balance = bob_acc_response.json()["accounts"][0]["balance"]
    assert bob_balance == "300.00"