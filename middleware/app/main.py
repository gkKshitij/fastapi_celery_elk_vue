from fastapi import Depends, FastAPI
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import get_session, init_db
from app.models import Song, SongCreate, Item, Book
##
import json
from pydantic import BaseModel
from fastapi import FastAPI

from app.worker import celery_app
##
from fastapi import FastAPI, HTTPException, Depends
from fastapi import Response
from fastapi.requests import Request
from pydantic import BaseModel, Field
from app import models
from app.database import engine, session_local, Base
from sqlalchemy.orm import Session
from app.routers import sample, items
####
import logging

import uvicorn
import uuid

from fastapi import FastAPI
from app.logging_setup import setup_root_logger

# setup root logger
setup_root_logger()

# Get logger for module
LOGGER = logging.getLogger(__name__)
LOGGER.info("---Starting App---")

####
app = FastAPI()


app.include_router(sample.router)
app.include_router(items.router)

@app.get("/random_uuid")
async def root():
    LOGGER.info(str(uuid.uuid4()))
    return "OK"


async def init_db():
# models.Base.metadata.create_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # session_local.add(
    #     User(username="testuser", password_hash=b"", password_salt=b"", balance=1)
    # )
    # session_local.commit()
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    print("Initialized the db")

##
if __name__ == "__main__":
    init_db()
# if __name__ == '__main__':
#     uvicorn.run(app, host="0.0.0.0", port=8000, log_config=None)