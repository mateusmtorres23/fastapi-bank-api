from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.database import engine
from app.models import Base
from app.routers.auth_router import router as auth_router
from app.routers.account_router import router as account_router
from app.routers.transaction_router import router as transaction_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Bank API", lifespan=lifespan)

app.include_router(auth_router)
app.include_router(account_router)
app.include_router(transaction_router)

@app.get("/")
def read_root():
    return {"message": "API Bancária Operacional", "version": "1.0.0"}