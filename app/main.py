from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.database import engine
from app.models import Base
from app.api.auth_router import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "API Operacional"}