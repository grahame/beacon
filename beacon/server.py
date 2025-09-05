from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db import create_db_and_tables
from .api import api


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(api)
