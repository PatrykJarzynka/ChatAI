from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from database import create_db_and_tables
from routers import role

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title='Role Service', lifespan=lifespan)

app.include_router(role.router)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info(f"Starting the application...")

    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8001)
