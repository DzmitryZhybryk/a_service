"""Module for storage authentication service routes"""
from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api import dependencies, schemas
from app.api import tasks
from app.api.handlers import AuthenticationHandlers
from app.utils.funcs import get_app_metadata

router = APIRouter()

BaseHandlerDep = Annotated[AuthenticationHandlers, Depends(dependencies.authentication_handler)]


@router.get("/", response_model=schemas.AppInfo, tags=["Index"])
async def index_page():
    application_metadata = await get_app_metadata()
    return application_metadata


@router.post("/registrate/", response_model=schemas.RegistrateResponse,
             responses=schemas.RegistrateUserResponse().detail, tags=["Authentication"])
async def registrate_user(user_data: schemas.RegistrateUser, handler: BaseHandlerDep):
    new_user = await handler.registrate_user(user_data=user_data)
    return new_user


@router.get("/registrate/activate/", status_code=status.HTTP_202_ACCEPTED, tags=["Authentication"])
def send_confirm_registration_email(email: str, username: str, confirm_key: str):
    tasks.send_confirm_registration_mail.delay(email=email, username=username, confirm_key=confirm_key)
    return {
        "status": 202,
        "data": "The later has been sent",
    }


@router.get("/registrate/activate/{key}/", response_model=schemas.ResponseToken, tags=["Authentication"])
async def confirm_registration(key: str, handler: BaseHandlerDep):
    tokens = await handler.confirm_registration(activate_key=key)
    return tokens
