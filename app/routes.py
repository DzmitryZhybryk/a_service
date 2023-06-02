"""Модуль для работы с роутами приложения."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app import dependencies
from app import schemas
from app.handlers import AuthenticationHandlers

router = APIRouter()

BaseHandlerDep = Annotated[AuthenticationHandlers, Depends(dependencies.authentication_handler)]


@router.get("/", response_model=schemas.AppInfo, tags=["Index"])
async def index_page(handle: BaseHandlerDep):
    application_metadata = await handle.get_metadata()
    return application_metadata
