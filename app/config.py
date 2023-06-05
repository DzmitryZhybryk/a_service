from pathlib import Path
from typing import Literal

from pydantic import BaseSettings

BASE_DIR = Path(__file__).parent.parent

RunModeType = Literal['dev', 'test', 'prod']


class BaseConfig(BaseSettings):
    database_url: str
    base_dir: Path = BASE_DIR
    pyproject_toml_path: Path = BASE_DIR / "pyproject.toml"

    class Config:
        env_file = BASE_DIR / ".env"


class LoggingConfig(BaseSettings):
    environment: str = "dev"
    run_mode: RunModeType = "dev"
    logging_dir: Path = BASE_DIR / "logs"
    sentry_activate: bool = False


logging_config = LoggingConfig()
base_config = BaseConfig()
