import pytest
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.services.account_service import create_user_account, get_next_sequence_number

@pytest.mark.asyncio
async def test_create_user_account_sequence_increment(db_session: AsyncSession):
    user = User(username="account_service_tester", password_hash="dummy_hash")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    next_seq = await get_next_sequence_number(user.id, db_session)
    assert next_seq == 1

    account1 = await create_user_account(user.id, db_session)
    
    await db_session.commit()
    await db_session.refresh(account1)

    assert account1.user_id == user.id
    assert account1.sequence_number == 1
    assert account1.balance == Decimal("0.00")

    next_seq_2 = await get_next_sequence_number(user.id, db_session)
    assert next_seq_2 == 2

    account2 = await create_user_account(user.id, db_session)
    await db_session.commit()
    await db_session.refresh(account2)

    assert account2.user_id == user.id
    assert account2.sequence_number == 2
    assert account2.balance == Decimal("0.00")