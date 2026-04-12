import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.db.database import get_db
from app.main import app

@pytest.mark.asyncio
async def test_create_user_model(db_session: AsyncSession):
    new_user = User(username="shannon_test", password_hash="mock_hash_123")
    db_session.add(new_user)
    await db_session.commit()
    await db_session.refresh(new_user)

    assert new_user.id is not None
    assert new_user.username == "shannon_test"

@pytest.mark.asyncio
async def test_user_unique_username_constraint(db_session: AsyncSession):

    user1 = User(username="unique_user", password_hash="hash1")
    db_session.add(user1)
    await db_session.commit()

    user2 = User(username="unique_user", password_hash="hash2")
    db_session.add(user2)
    
    with pytest.raises(IntegrityError):
        await db_session.commit()