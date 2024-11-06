import json

from fastapi import Depends, APIRouter 
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.logging_setup import setup_root_logger
from app.db import get_session#, init_db
from app.models import Song, SongCreate, Item
from app.worker import celery_app

import logging
# setup root logger
setup_root_logger()
# Get logger for module
LOGGER = logging.getLogger(__name__)
LOGGER.info("---in sample file---")

router = APIRouter()


@router.get("/ping")
async def pong():
    LOGGER.info("---try ping---")
    return {"ping": "pong!"}


@router.get("/songs", response_model=list[Song])
async def get_songs(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Song))
    songs = result.scalars().all()
    return [Song(name=song.name, artist=song.artist, year=song.year, id=song.id) for song in songs]


@router.post("/songs")
async def add_song(song: SongCreate, session: AsyncSession = Depends(get_session)):
    song = Song(name=song.name, artist=song.artist, year=song.year)
    session.add(song)
    await session.commit()
    await session.refresh(song)
    return song


@router.post("/task_hello_world/")
async def create_item(item: Item):
    # celery task name
    task_name = "hello.task"
    # send task to celery
    task = celery_app.send_task(task_name, args=[item.name])

    # return task id and url
    return dict(
        id=task.id,
        url=f"localhost:5000/check_task/{task.id}",
    )


@router.get("/check_task/{id}")
def check_task(id: str):
    # get celery task from id
    task = celery_app.AsyncResult(id)

    # if task is in success state
    if task.state == "SUCCESS":
        response = {
            "status": task.state,
            "result": task.result,
            "task_id": id,
        }

    # if task is in failure state
    elif task.state == "FAILURE":
        response = json.loads(
            task.backend.get(
                task.backend.get_key_for_task(task.id),
            ).decode("utf-8")
        )
        del response["children"]
        del response["traceback"]

    # if task is in other state
    else:
        response = {
            "status": task.state,
            "result": task.info,
            "task_id": id,
        }

    # return response
    return response