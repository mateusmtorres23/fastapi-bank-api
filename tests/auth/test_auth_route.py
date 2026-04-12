import pytest
from httpx import AsyncClient
from fastapi import status

@pytest.mark.asyncio
async def test_route_register_user_success(async_client: AsyncClient):
    payload = {"username": "route_user", "password": "route_password"}
    response = await async_client.post("/auth/register", json=payload)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["username"] == "route_user"
    assert "id" in data
    assert "password" not in data

@pytest.mark.asyncio
async def test_route_register_user_duplicate(async_client: AsyncClient):
    payload = {"username": "duplicate_route", "password": "password123"}
    await async_client.post("/auth/register", json=payload)
    
    response = await async_client.post("/auth/register", json=payload)
    assert response.status_code == status.HTTP_409_CONFLICT

@pytest.mark.asyncio
async def test_route_login_success(async_client: AsyncClient):
    reg_payload = {"username": "login_user", "password": "correct_password"}
    await async_client.post("/auth/register", json=reg_payload)
    
    login_data = {"username": "login_user", "password": "correct_password"}
    response = await async_client.post("/auth/token", data=login_data)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_route_login_invalid_credentials(async_client: AsyncClient):
    login_data = {"username": "non_existent", "password": "wrong_password"}
    response = await async_client.post("/auth/token", data=login_data)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Incorrect username or password"