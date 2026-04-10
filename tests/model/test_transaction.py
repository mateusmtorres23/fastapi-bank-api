import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.model.user import User
from app.model.account import Account
from app.model.transaction import Transaction
from app.model.transaction import TransactionType

@pytest.mark.asyncio
async def test_create_transaction_timestamp(db_session: AsyncSession):
    owner = User(username="transaction_owner", password_hash="owner_pw")
    db_session.add(owner)
    await db_session.commit()
    await db_session.refresh(owner)

    account = Account(user_id=owner.id)
    db_session.add(account)
    await db_session.commit()
    await db_session.refresh(account)

    transaction = Transaction(account_id=account.id, amount=100.00, type=TransactionType.DEPOSIT)
    db_session.add(transaction)
    await db_session.commit()
    await db_session.refresh(transaction)

    assert transaction.id is not None
    assert float(transaction.amount) == 100.00
    assert transaction.type == TransactionType.DEPOSIT
    assert transaction.timestamp is not None