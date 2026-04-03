from fastapi import FastAPI
from app.routers import users

app = FastAPI(title="Workshop API", version="1.0.0")

app.include_router(users.router, prefix="/users", tags=["users"])


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": app.version}
