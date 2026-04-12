import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schema import UserCreate
from app.services.auth_service import register_user, authenticate_user

class MockCredentials:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

@pytest.mark.asyncio
async def test_register_user_success(db_session: AsyncSession):
    user_data = UserCreate(username="test_user", password="secure_password")
    user = await register_user(user_data, db_session)
    
    assert user.id is not None
    assert user.username == "test_user"
    assert user.password_hash != "secure_password"

@pytest.mark.asyncio
async def test_register_user_duplicate_username(db_session: AsyncSession):
    user_data = UserCreate(username="test_user", password="secure_password")
    await register_user(user_data, db_session)
    
    with pytest.raises(HTTPException) as exc_info:
        await register_user(user_data, db_session)
    
    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "Username already registered"

@pytest.mark.asyncio
async def test_authenticate_user_success(db_session: AsyncSession):
    user_data = UserCreate(username="test_user", password="login_password")
    await register_user(user_data, db_session)
    
    credentials = MockCredentials(username="test_user", password="login_password")
    authenticated_user = await authenticate_user(credentials.username, credentials.password, db_session) # type: ignore
    
    assert authenticated_user is not None
    assert authenticated_user.username == "test_user"

@pytest.mark.asyncio
async def test_authenticate_user_invalid_password(db_session: AsyncSession):
    user_data = UserCreate(username="test_user", password="correct_password")
    await register_user(user_data, db_session)
    
    credentials = MockCredentials(username="test_user", password="wrong_password")
    authenticated_user = await authenticate_user(credentials.username, credentials.password, db_session) # type: ignore
    
    assert authenticated_user is None

@pytest.mark.asyncio
async def test_authenticate_user_not_found(db_session: AsyncSession):
    credentials = MockCredentials(username="ghost_user", password="password")
    authenticated_user = await authenticate_user(credentials.username, credentials.password, db_session) # type: ignore
    
    assert authenticated_user is None