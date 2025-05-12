from fastapi import FastAPI
from contextlib import asynccontextmanager

from database import create_db_and_tables
from routers import role

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title='Role Service', lifespan=lifespan)

app.include_router(role.router)
