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
from app.database import engine, session_local
from sqlalchemy.orm import Session
import app

# Dependency
def get_db(request: Request):
    return request.state.db


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = session_local()
        response = await call_next(request)
        response_body = b''
        if all(filter not in request.url.__str__() for filter in ['docs', 'openapi.json', 'favicon.ico']):
            async for chunk in response.body_iterator:
                response_body += chunk
            response = Response(content=response_body, status_code=response.status_code,
                                headers=dict(response.headers), media_type=response.media_type)
            await store_audit_middleware(request, response_body, request.state.db)
    finally:
        request.state.db.close()
    return response


async def store_audit_middleware(request: Request, response_body, db):
    audit_entry = models.Audit()
    audit_entry.url = request.url.__str__()
    audit_entry.headers = request.headers.items()
    audit_entry.method = request.method
    audit_entry.response = response_body.decode()
    db.add(audit_entry)
    db.commit()
    return audit_entry