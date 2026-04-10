from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.database import engine
from app.model import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "API Operacional"}