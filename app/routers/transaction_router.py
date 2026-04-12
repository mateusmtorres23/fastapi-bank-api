from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.user import User
from app.models.transaction import TransactionType
from app.schemas.transaction_schema import TransactionCreate, TransferCreate, TransactionRead
from app.services.transaction_service import execute_transaction, execute_transfer
from app.security.auth_manager import get_current_user

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/deposit", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
async def deposit(
    data: TransactionCreate, 
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await execute_transaction(
        user_id=current_user.id,
        sequence_number=data.account_sequence_number,
        amount=data.amount,
        transaction_type=TransactionType.DEPOSIT,
        db_session=db
    )

@router.post("/withdraw", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
async def withdraw(
    data: TransactionCreate, 
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await execute_transaction(
        user_id=current_user.id,
        sequence_number=data.account_sequence_number,
        amount=data.amount,
        transaction_type=TransactionType.WITHDRAWAL,
        db_session=db
    )

@router.post("/transfer", status_code=status.HTTP_200_OK)
async def transfer(
    data: TransferCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await execute_transfer(
        source_user_id=current_user.id,
        source_sequence=data.source_sequence_number,
        dest_user_id=data.destination_user_id,
        dest_sequence=data.destination_sequence_number,
        amount=data.amount,
        db_session=db
    )