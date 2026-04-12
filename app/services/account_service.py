from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.account import Account
from decimal import Decimal

async def get_next_sequence_number(user_id: int, db_session: AsyncSession) -> int:
    stmt = select(func.count(Account.sequence_number)).where(Account.user_id == user_id)
    result = await db_session.execute(stmt)
    count = result.scalar() or 0
    return count + 1

async def create_user_account(user_id: int, db_session: AsyncSession) -> Account:    
    seq_num = await get_next_sequence_number(user_id, db_session)
    
    new_account = Account(
        user_id=user_id,
        sequence_number=seq_num,
        balance=Decimal("0.00")
    )
    
    db_session.add(new_account)
    return new_account