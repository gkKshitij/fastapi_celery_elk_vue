import logging

from app.logging_setup import setup_root_logger

from fastapi import Depends, FastAPI
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import get_session#, init_db
from app.models import Song, SongCreate
from app.routers import sample, items
from app.worker import celery_app

# setup root logger
setup_root_logger()

# Get logger for module
LOGGER = logging.getLogger(__name__)
LOGGER.info("---Starting App---")

####
app = FastAPI()

app.include_router(sample.router)
app.include_router(items.router)

# # # only for the first time for initializing alembic
# @app.on_event("startup")
# async def on_startup():
#     await init_db()