from datetime import date, datetime
from enum import Enum
from pathlib import Path

from email_validator import validate_email
from fastapi import status
from pydantic import BaseModel, validator

from app.config import RunModeType


class AppMetadata(BaseModel):
    """Pydantic model describe application metadata"""
    name: str
    version: str
    description: str


class RoleEnum(str, Enum):
    admin = "admin"
    moderator = "moderator"
    base_user = "base_user"


class UserBase(BaseModel):
    username: str
    nickname: str
    email: str
    first_name: str | None = None
    last_name: str | None = None
    birthday: date | None = None
    role: RoleEnum
