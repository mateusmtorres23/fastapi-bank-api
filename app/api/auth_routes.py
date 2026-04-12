from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas.user_schema import UserCreate, UserRead
from app.services.auth_service import register_user, authenticate_user
from app.security.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db_session: AsyncSession = Depends(get_db)):
    return await register_user(user_data, db_session)

@router.post("/token")
async def login_for_access_token(credentials: OAuth2PasswordRequestForm = Depends(), db_session: AsyncSession = Depends(get_db)):
    user = await authenticate_user(credentials, db_session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}