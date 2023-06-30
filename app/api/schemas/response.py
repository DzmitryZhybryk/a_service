"""Module for storage pydantic models"""
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel

from app.api.schemas.base import UserBase, AppMetadata
from app.config import RunModeType


class AppInfo(AppMetadata):
    """Pydantic model describe detail application metadata. Used as a response model for index_page rout"""
    environment: str
    run_mode: RunModeType
    logs_dir: Path


class Registrate(BaseModel):
    confirm_registration_key: str
    username: str
    email: str


class GetUser(UserBase):
    id: int
    main_photo: str | None
    activated_at: bool | None
    created_date: datetime
    is_user_activate: bool
    updated_date: datetime | None
    role: object


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
