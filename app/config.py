"""Module for storage config classes"""
from pathlib import Path
from typing import Literal

from pydantic import BaseSettings, validator

BASE_DIR = Path(__file__).parent.parent

RunModeType = Literal['dev', 'test', 'prod']


class DatabaseConfig(BaseSettings):
    database_url: str
    postgres_echo: bool = False
    redis_host: str
    redis_username: str
    redis_password: str
    redis_hash_key: str
    digestmod: str
    redis_token_db: int

    class Config:
        env_file = BASE_DIR / ".env"


class BaseConfig(BaseSettings):
    user_roles: str | tuple
    base_dir: Path = BASE_DIR
    pyproject_toml_path: Path = BASE_DIR / "pyproject.toml"
    confirm_registration_url: str = "http://127.0.0.1:8001/api/v1/registrate/activate/"

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


class SecretConfig(BaseSettings):
    secret_key: str
    salt: str
    jwt_algorithm: str
    access_token_expire: int  # minutes
    refresh_token_expire: int  # days

    class Config:
        env_file = BASE_DIR / '.env'


class LoggingConfig(BaseSettings):
    environment: str = "dev"
    run_mode: RunModeType = "dev"
    logging_dir: Path = BASE_DIR / "logs"
    sentry_activate: bool = False


class EmailConfig(BaseSettings):
    smtp_server_host: str = "smtp.gmail.com"
    smtp_server_port: int = 587
    work_email: str
    work_email_password: str

    class Config:
        env_file = BASE_DIR / ".env"


logging_config = LoggingConfig()
base_config = BaseConfig()
email_config = EmailConfig()
init_config = InitUserData()
secret_config = SecretConfig()
database_config = DatabaseConfig()
