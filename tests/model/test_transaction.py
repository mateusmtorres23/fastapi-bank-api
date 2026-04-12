import pytest
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.account import Account
from app.models.transaction import Transaction, TransactionType

@pytest.mark.asyncio
async def test_create_transaction_timestamp(db_session: AsyncSession):
    owner = User(username="transaction_owner", password_hash="owner_pw")
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

    transaction = Transaction(
        user_id=owner.id, 
        account_sequence_number=account.sequence_number, 
        amount=Decimal("100.00"), 
        type=TransactionType.DEPOSIT
    )
    db_session.add(transaction)
    await db_session.commit()
    await db_session.refresh(transaction)

    assert transaction.id is not None
    assert transaction.amount == Decimal("100.00")
    assert transaction.type == TransactionType.DEPOSIT
    assert transaction.timestamp is not None