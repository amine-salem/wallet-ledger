from fastapi import FastAPI

app = FastAPI(title="Wallet Ledger")

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}