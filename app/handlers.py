from app.services import AuthenticationStorage
from app import schemas
from app.config import logging_config


class AuthenticationHandlers:

    def __init__(self, storage: AuthenticationStorage):
        self.__services = storage

    async def get_metadata(self) -> schemas.AppInfo:
        application_metadata = await self.__services.get_app_metadata()
        response_schema = schemas.AppInfo(name=application_metadata.name, version=application_metadata.version,
                                          description=application_metadata.description,
                                          environment=logging_config.environment, run_mode=logging_config.run_mode,
                                          logs_dir=logging_config.logging_dir)
        return response_schema
