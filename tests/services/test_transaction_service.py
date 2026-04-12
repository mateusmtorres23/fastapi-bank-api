import pytest
from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.transaction import TransactionType
from app.schemas.user_schema import UserCreate
from app.services.auth_service import register_user
from app.services.transaction_service import execute_transaction, execute_transfer, get_account

@pytest.mark.asyncio
async def test_banking_flow(db_session: AsyncSession):
    joao = await register_user(UserCreate(username="joao", password="password123"), db_session)
    maria = await register_user(UserCreate(username="maria", password="password123"), db_session)

    conta_joao = await get_account(joao.id, 1, db_session)
    conta_maria = await get_account(maria.id, 1, db_session)
    
    assert conta_joao.balance == Decimal("0.00")
    assert conta_maria.balance == Decimal("0.00")

    await execute_transaction(
        user_id=joao.id, 
        sequence_number=1, 
        amount=Decimal("1000.00"), 
        transaction_type=TransactionType.DEPOSIT, 
        db_session=db_session
    )
    
    await db_session.refresh(conta_joao)
    assert conta_joao.balance == Decimal("1000.00")

    with pytest.raises(HTTPException) as exc_info:
        await execute_transaction(
            user_id=joao.id, 
            sequence_number=1, 
            amount=Decimal("1500.00"), 
            transaction_type=TransactionType.WITHDRAWAL, 
            db_session=db_session
        )
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Insufficient funds."

    await execute_transfer(
        source_user_id=joao.id,
        source_sequence=1,
        dest_user_id=maria.id,
        dest_sequence=1,
        amount=Decimal("300.00"),
        db_session=db_session
    )

    await db_session.refresh(conta_joao)
    await db_session.refresh(conta_maria)
    
    assert conta_joao.balance == Decimal("700.00")  # 1000 - 300
    assert conta_maria.balance == Decimal("300.00") # 0 + 300