from fastapi import HTTPException, status
from starlette.concurrency import run_in_threadpool
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from pwdlib import PasswordHash
from app.schemas.user_schema import UserCreate
from app.models import User

password_hash = PasswordHash.recommended()
async def get_password_hash(password: str):
    return await run_in_threadpool(password_hash.hash, password)

async def verify_password(plain_password: str, hashed_password: str):
    return await run_in_threadpool(password_hash.verify, plain_password, hashed_password)


async def register_user(user_data: UserCreate, db_session: AsyncSession) -> User:
    password_hash = await get_password_hash(user_data.password)
    new_user = User(username=user_data.username, password_hash=password_hash)
    db_session.add(new_user)
    
    try:
        await db_session.commit()
        await db_session.refresh(new_user)
        return new_user
    except IntegrityError:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already registered"
        )

async def authenticate_user(username: str, password: str, db_session: AsyncSession) -> User | None:
    stmt = select(User).where(User.username == username)
    result = await db_session.execute(stmt)
    user = result.scalars().first()
    
    if user and await verify_password(password, user.password_hash):
        return user
    return None