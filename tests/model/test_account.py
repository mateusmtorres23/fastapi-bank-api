import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.account import Account
@pytest.mark.asyncio
async def test_create_account_and_relationship(db_session: AsyncSession):
    owner = User(username="owner", password_hash="owner_pw")
    db_session.add(owner)
    await db_session.commit()
    await db_session.refresh(owner)

    account = Account(user_id=owner.id)
    db_session.add(account)
    await db_session.commit()
    await db_session.refresh(account)

    assert account.id is not None
    assert account.balance == 0.0
    assert account.user_id == owner.id
