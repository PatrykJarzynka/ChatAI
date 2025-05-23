from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import files_router
from database import create_db_and_tables
from routers import chat_router, auth_router, user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:80",
    "http://localhost:4200",
    'http://127.0.0.1:8000',
    'http://patryk-jarzynka.codeconcept.pl'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router.router)
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(files_router.router)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info(f"Starting the application...")

    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)