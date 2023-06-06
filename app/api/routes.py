"""Module for storage authentication service routes"""
from typing import Annotated

from fastapi import APIRouter, Depends

from app.api import dependencies, schemas
from app.api.handlers import AuthenticationHandlers
from app.utils.funcs import get_app_metadata

router = APIRouter()

BaseHandlerDep = Annotated[AuthenticationHandlers, Depends(dependencies.authentication_handler)]


@router.get("/", response_model=schemas.AppInfo, tags=["Index"])
async def index_page():
    application_metadata = await get_app_metadata()
    return application_metadata
