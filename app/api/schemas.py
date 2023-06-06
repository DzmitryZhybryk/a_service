"""Module for storage pydantic models"""
from pydantic import BaseModel
from pathlib import Path
from app.config import RunModeType


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


class IncorrectLoginData(BaseModel):
    """Pydantic model describe incorrect username or password response"""
    detail: str = "Incorrect username or password"
