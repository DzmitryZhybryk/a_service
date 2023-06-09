"""Module for storage config classes"""
from pathlib import Path
from typing import Literal

from pydantic import BaseSettings, validator

BASE_DIR = Path(__file__).parent.parent

RunModeType = Literal['dev', 'test', 'prod']


class BaseConfig(BaseSettings):
    user_roles: str | tuple
    database_url: str
    postgres_echo: bool = False
    base_dir: Path = BASE_DIR
    pyproject_toml_path: Path = BASE_DIR / "pyproject.toml"

    class Config:
        env_file = BASE_DIR / ".env"

    @validator('user_roles')
    def make_tuple(cls, user_roles: str):
        user_roles = tuple(user_roles.split(","))
        return user_roles


class InitUserData(BaseSettings):
    password: str
    username: str = "admin"
    email: str = "admin@gmail.com"
    nickname: str = "admin"
    role: str = "admin"

    class Config:
        env_file = BASE_DIR / ".env"


class InitConfig(InitUserData):
    pass

    class Config:
        env_file = BASE_DIR / ".env"


class LoggingConfig(BaseSettings):
    environment: str = "dev"
    run_mode: RunModeType = "dev"
    logging_dir: Path = BASE_DIR / "logs"
    sentry_activate: bool = False


logging_config = LoggingConfig()
base_config = BaseConfig()
init_config = InitConfig()
