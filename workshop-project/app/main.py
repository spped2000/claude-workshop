from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from app.routers import users

GZIP_MINIMUM_SIZE = 1000

app = FastAPI(title="Workshop API", version="1.0.0")

app.add_middleware(GZipMiddleware, minimum_size=GZIP_MINIMUM_SIZE)

app.include_router(users.router, prefix="/users", tags=["users"])


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": app.version}
