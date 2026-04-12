from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from app.db.database import get_db
from app.models.user import User
from app.schemas.user_schema import UserReadWithAccounts
from app.security.auth_manager import get_current_user

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.get("/me", response_model=UserReadWithAccounts)
async def get_my_accounts(
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    stmt = select(User).where(User.id == current_user.id).options(selectinload(User.accounts))
    result = await db.execute(stmt)
    return result.scalars().first()