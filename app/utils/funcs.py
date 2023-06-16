"""Module for storage utils funcs"""
import random
import string
from datetime import datetime, timezone
from string import Template

from app.api import schemas
from app.config import config
from app.utils.file_worker import TomlWorker


def __get_metadata_from_dict(project_data: dict) -> schemas.AppMetadata:
    """
    Function finds app metadata in the dict

    Args:
        project_data: dict with app metadata

    Returns:
        pydantic model with app metadata

    """
    app_name = project_data.get("project").get("name")
    app_version = project_data.get("project").get("version")
    app_description = project_data.get("project").get("description")
    response_schema = schemas.AppMetadata(name=app_name, version=app_version,
                                          description=app_description)
    return response_schema


async def get_app_metadata() -> schemas.AppInfo:
    """
    Function builds app metadata from pyproject.toml file

    Returns:
        pydantic model with all app information

    """
    toml_worker = TomlWorker(config.init.pyproject_toml_path)
    data_from_pyproject_toml = await toml_worker.read_file()
    app_metadata = __get_metadata_from_dict(project_data=data_from_pyproject_toml)
    response_schema = schemas.AppInfo(name=app_metadata.name, version=app_metadata.version,
                                      description=app_metadata.description,
                                      environment=config.logging.environment, run_mode=config.logging.run_mode,
                                      logs_dir=config.logging.logging_dir)
    return response_schema


def get_current_time_with_utc() -> datetime:
    """
    Function return current time with utc

    Returns:
        current time with utc

    """
    return datetime.now(timezone.utc)


def __make_rout_with_path(url: str, template: Template, **args) -> str:
    """
    Function concatenate rout url and path param

    Args:
        url: rout url
        path_param: path param

    Returns:
        concatenated url and path param

    """
    template = template
    result = template.substitute(base_url=url, **args)
    return result


def make_confirm_registration_key(_range: int) -> str:
    """
    Function generate random string

    Args:
        _range: len string for generate

    Returns:
        generated string

    """
    symbols = f"{string.ascii_lowercase}{string.ascii_uppercase}{string.digits}"
    rand_code = ''.join(random.choice(symbols) for _ in range(_range))
    return rand_code


def make_confirm_registration_url(key: str) -> str:
    """
    Function makes url for confirm user registration

    Args:
        key: confirm registration key. With this key you can find user id in redis database

    Returns:
        url for confirm new user registration

    """
    template = Template("$base_url$key/")
    base_url = config.init.confirm_registration_url
    result_url = __make_rout_with_path(url=base_url, template=template, key=key)
    return result_url


def make_confirm_registration_message(username: str, confirm_registration_url: str) -> str:
    """
    Function makes an email message that will be sent to the user for confirm registration

    Args:
        username: user username
        confirm_registration_url: url for confirm registration

    Returns:
        confirm registration message

    """
    message = f"Welcome {username}! Thanks for registration! Confirm registration link: {confirm_registration_url}"
    return message
