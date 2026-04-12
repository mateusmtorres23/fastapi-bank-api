from decimal import Decimal
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.account import Account
from app.models.transaction import Transaction, TransactionType

async def get_account(user_id: int, sequence_number: int, db_session: AsyncSession) -> Account:
    stmt = select(Account).where(
        Account.user_id == user_id, 
        Account.sequence_number == sequence_number
    )
    result = await db_session.execute(stmt)
    account = result.scalars().first()
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Account {sequence_number} for user {user_id} not found."
        )
    return account

async def execute_transaction(
    user_id: int, 
    sequence_number: int, 
    amount: Decimal, 
    transaction_type: TransactionType, 
    db_session: AsyncSession
) -> Transaction:
    account = await get_account(user_id, sequence_number, db_session)

    if transaction_type == TransactionType.WITHDRAWAL:
        if account.balance < amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Insufficient funds."
            )
        account.balance -= amount
    elif transaction_type == TransactionType.DEPOSIT:
        account.balance += amount

    transaction = Transaction(
        user_id=user_id,
        account_sequence_number=sequence_number,
        amount=amount,
        type=transaction_type
    )
    
    db_session.add(transaction)
    await db_session.commit()
    await db_session.refresh(transaction)
    return transaction

async def execute_transfer(
    source_user_id: int, 
    source_sequence: int, 
    dest_user_id: int, 
    dest_sequence: int, 
    amount: Decimal, 
    db_session: AsyncSession
):
    source_account = await get_account(source_user_id, source_sequence, db_session)
    dest_account = await get_account(dest_user_id, dest_sequence, db_session)

    if source_account.balance < amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Insufficient funds for transfer."
        )

    source_account.balance -= amount
    dest_account.balance += amount

    withdrawal = Transaction(
        user_id=source_user_id,
        account_sequence_number=source_sequence,
        amount=amount,
        type=TransactionType.WITHDRAWAL
    )
    deposit = Transaction(
        user_id=dest_user_id,
        account_sequence_number=dest_sequence,
        amount=amount,
        type=TransactionType.DEPOSIT
    )

    db_session.add_all([withdrawal, deposit])
    
    await db_session.commit()
    return {"message": "Transfer successful"}