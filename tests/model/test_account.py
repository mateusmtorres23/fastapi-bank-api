import pytest
from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.account import Account

@pytest.mark.asyncio
async def test_create_account_weak_entity_relationship(db_session: AsyncSession):
    owner = User(username="owner", password_hash="owner_pw")
    db_session.add(owner)
    await db_session.commit()
    await db_session.refresh(owner)

    account = Account(
        user_id=owner.id, 
        sequence_number=1, 
        balance=Decimal("0.00")
    )
    db_session.add(account)
    await db_session.commit()
    await db_session.refresh(account)

    assert account.user_id == owner.id
    assert account.sequence_number == 1
    assert account.balance == Decimal("0.00")
    
    stmt = select(User).where(User.id == owner.id).options(selectinload(User.accounts))
    result = await db_session.execute(stmt)
    owner_with_accounts = result.scalars().first()
    
    assert owner_with_accounts is not None
    assert len(owner_with_accounts.accounts) == 1
    assert owner_with_accounts.accounts[0].sequence_number == 1