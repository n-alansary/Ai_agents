from contextlib import asynccontextmanager
from fastapi import FastAPI
from routes.chat import router as chat_router
from utils.db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database connection on app startup
    await init_db()
    yield

app = FastAPI(title="Squash Agent API", lifespan=lifespan)

app.include_router(chat_router)

