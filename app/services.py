from app import schemas
from app.utils.file_reader import toml_worker


class AuthenticationStorage:

    def __init__(self):
        pass

    @staticmethod
    def __get_metadata_from_dict(project_data: dict) -> schemas.AppMetadata:
        app_name = project_data.get("project").get("name")
        app_version = project_data.get("project").get("version")
        app_description = project_data.get("project").get("description")
        response_schema = schemas.AppMetadata(name=app_name, version=app_version,
                                              description=app_description)
        return response_schema

    async def get_app_metadata(self) -> schemas.AppMetadata:
        data_from_pyproject_toml = await toml_worker.read_file()
        app_metadata = self.__get_metadata_from_dict(project_data=data_from_pyproject_toml)
        return app_metadata
