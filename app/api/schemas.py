from pydantic import BaseModel
from pathlib import Path
from app.config import RunModeType


class AppMetadata(BaseModel):
    name: str
    version: str
    description: str


class AppInfo(AppMetadata):
    environment: str
    run_mode: RunModeType
    logs_dir: Path
