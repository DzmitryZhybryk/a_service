"""Module for storage authentication service routes"""
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import status

from app.api import dependencies, schemas
from app.api.handlers import AuthenticationHandlers
from app.utils.funcs import get_app_metadata

router = APIRouter()

BaseHandlerDep = Annotated[AuthenticationHandlers, Depends(dependencies.authentication_handler)]


@router.get("/",
            response_model=schemas.response.AppInfo,
            responses=schemas.example.base_responses,
            dependencies=[Depends(dependencies.get_api_key)],
            tags=["Index"])
async def index_page():
    application_metadata = await get_app_metadata()
    return application_metadata


@router.post("/registrate/",
             status_code=status.HTTP_201_CREATED,
             response_model=schemas.response.Registrate,
             responses=schemas.example.registrate_response,
             dependencies=[Depends(dependencies.get_api_key)],
             tags=["Authentication"])
async def registrate_user(user_data: schemas.request.RegistrateUser, handler: BaseHandlerDep):
    new_user = await handler.registrate_user(user_data=user_data)
    return new_user


@router.get("/registrate/activate/",
            status_code=status.HTTP_202_ACCEPTED,
            responses=schemas.example.base_responses,
            dependencies=[Depends(dependencies.get_api_key)],
            tags=["Authentication"])
def confirm_registration(email: str, username: str, confirm_key: str, handler: BaseHandlerDep):
    handler.confirm_registration(email=email, username=username, confirm_key=confirm_key)
    return {
        "data": "The later has been sent",
    }


@router.get("/registrate/activate/{key}/",
            response_model=schemas.response.Token,
            responses=schemas.example.base_responses,
            tags=["Authentication"])
async def activate_user(key: str, handler: BaseHandlerDep):
    tokens = await handler.activate_user(activate_key=key)
    return tokens


@router.get("/users/{user_id}/",
            response_model=schemas.response.GetUser,
            responses=schemas.example.get_user_response,
            dependencies=[Depends(dependencies.get_api_key)],
            tags=["Authentication"])
async def get_user(user_id: int, handler: BaseHandlerDep):
    user = await handler.get_user(user_id=user_id)
    return user
