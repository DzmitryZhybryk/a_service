"""Module for storage pydantic models"""
from datetime import date
from enum import Enum
from pathlib import Path
from fastapi import status
from email_validator import validate_email
from pydantic import BaseModel, validator

from app.config import RunModeType


class RoleEnum(str, Enum):
    admin = "admin"
    moderator = "moderator"
    base_user = "base_user"


class RegistrateUser(BaseModel):
    username: str
    password: str
    confirm_password: str
    nickname: str
    email: str
    first_name: str | None = None
    last_name: str | None = None
    birthday: date | None = None
    role: RoleEnum = "base_user"

    @validator("confirm_password")
    def passwords_match(cls, confirm_password: str, values: dict) -> str:
        if "password" in values and confirm_password != values["password"]:
            raise ValueError("Password mismatch!")

        return confirm_password

    @validator("email")
    def validate_email(cls, email: str) -> str:
        validate_email(email)
        return email

    class Config:
        schema_extra = {
            "example": {
                "username": "admin",
                "password": "somedifficultpassword",
                "confirm_password": "somedifficultpassword",
                "nickname": "BigDaddy",
                "email": "my_email@gmail.com",
                "first_name": "Jon",
                "last_name": "Smith",
                "birthday": "2023-06-08",
                "user_role": "base_user"
            }
        }


class ResponseToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class AppMetadata(BaseModel):
    """Pydantic model describe application metadata"""
    name: str
    version: str
    description: str


class AppInfo(AppMetadata):
    """Pydantic model describe detail application metadata. Used as a response model for index_page rout"""
    environment: str
    run_mode: RunModeType
    logs_dir: Path


class Conflict(BaseModel):
    """Pydantic модель описывает ответ, при попытке создать пользователя с данными, которые уже есть в базе данных"""
    detail: dict = {
        "message": "The same data already exist in database"
    }


class RegistrateUserResponse(BaseModel):
    detail: dict = {
        status.HTTP_409_CONFLICT: {
            "description": "User with this data already exist in database",
            "model": Conflict
        }
    }


class IncorrectLoginData(BaseModel):
    """Pydantic model describe incorrect username or password response"""
    detail: str = "Incorrect username or password"
