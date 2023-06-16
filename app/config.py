"""Module for storage config classes"""
from pathlib import Path
from typing import Literal

from pydantic import BaseSettings, validator

BASE_DIR = Path(__file__).parent.parent

RunModeType = Literal['dev', 'test', 'prod']


class BaseConfigMixin:
    env_file = BASE_DIR / ".env"


class Database(BaseSettings):
    database_url: str
    postgres_echo: bool = False

    redis_host: str
    redis_username: str
    redis_password: str
    redis_hash_key: str
    digestmod: str
    redis_database: int

    class Config(BaseConfigMixin):
        pass


class InitData(BaseSettings):
    password: str
    username: str = "admin"
    email: str = "admin@gmail.com"
    nickname: str = "admin"
    role: str = "admin"
    user_roles: str | tuple
    base_dir: Path = BASE_DIR
    pyproject_toml_path: Path = BASE_DIR / "pyproject.toml"
    confirm_registration_url: str = "http://127.0.0.1:8001/api/v1/registrate/activate/"

    @validator('user_roles')
    def make_tuple(cls, user_roles: str):
        user_roles = tuple(user_roles.split(","))
        return user_roles

    class Config(BaseConfigMixin):
        pass


class Secret(BaseSettings):
    secret_key: str
    salt: str
    jwt_algorithm: str
    access_token_expire: int  # minutes
    refresh_token_expire: int  # days

    class Config(BaseConfigMixin):
        pass


class Logging(BaseSettings):
    environment: str = "dev"
    run_mode: RunModeType = "dev"
    logging_dir: Path = BASE_DIR / "logs"
    sentry_activate: bool = False
    loguru_level: str = "INFO"

    class Config(BaseConfigMixin):
        pass


class Email(BaseSettings):
    smtp_server_host: str = "smtp.gmail.com"
    smtp_server_port: int = 587
    work_email: str
    work_email_password: str

    class Config(BaseConfigMixin):
        pass


class Rabbitmq(BaseSettings):
    rabbitmq_default_user: str = "admin"
    rabbitmq_default_pass: str = "admin"
    rabbitmq_backend: str = "rpc://"

    class Config(BaseConfigMixin):
        pass


class ConfigStorage:

    def __init__(self):
        self.logging = Logging()
        self.email = Email()
        self.init = InitData()
        self.secret = Secret()
        self.database = Database()
        self.rabbitmq = Rabbitmq()


config = ConfigStorage()
