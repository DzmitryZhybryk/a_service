from app.api import schemas
from app.config import base_config, logging_config
from app.utils.file_worker import TomlWorker
from datetime import datetime, timezone


def __get_metadata_from_dict(project_data: dict) -> schemas.AppMetadata:
    app_name = project_data.get("project").get("name")
    app_version = project_data.get("project").get("version")
    app_description = project_data.get("project").get("description")
    response_schema = schemas.AppMetadata(name=app_name, version=app_version,
                                          description=app_description)
    return response_schema


async def get_app_metadata() -> schemas.AppInfo:
    toml_worker = TomlWorker(base_config.pyproject_toml_path)
    data_from_pyproject_toml = await toml_worker.read_file()
    app_metadata = __get_metadata_from_dict(project_data=data_from_pyproject_toml)
    response_schema = schemas.AppInfo(name=app_metadata.name, version=app_metadata.version,
                                      description=app_metadata.description,
                                      environment=logging_config.environment, run_mode=logging_config.run_mode,
                                      logs_dir=logging_config.logging_dir)
    return response_schema


def get_current_time_with_utc() -> datetime:
    """
    Функция для получения текущего времени с UTC

    Returns:
        Текущее время

    """
    return datetime.now(timezone.utc)
