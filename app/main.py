from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.db import get_session

app = FastAPI(title="Wallet Ledger")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/health/db")
async def health_db(session: AsyncSession = Depends(get_session)) -> dict[str, str]:
    await session.execute(text("Select 1"))
    return {"status": "ok", "database": "connected"}