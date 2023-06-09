"""Module for storage authentication service routes"""
from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api import dependencies, schemas
from app.api.handlers import AuthenticationHandlers
from app.utils.funcs import get_app_metadata

router = APIRouter()

BaseHandlerDep = Annotated[AuthenticationHandlers, Depends(dependencies.authentication_handler)]


@router.get("/", response_model=schemas.AppInfo, tags=["Index"])
async def index_page():
    application_metadata = await get_app_metadata()
    return application_metadata


@router.post("/registrate/", status_code=status.HTTP_204_NO_CONTENT, responses=schemas.RegistrateUserResponse().detail,
             tags=["Authentication"])
async def registrate_user(user_data: schemas.RegistrateUser, handler: BaseHandlerDep):
    await handler.registrate_user(user_data=user_data)


@router.get("/registrate/activate/{email}/")
async def confirm_registration(email: str, handler: BaseHandlerDep):
    await handler.confirm_registration(email=email)
