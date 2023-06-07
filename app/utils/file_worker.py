from abc import ABC, abstractmethod
from typing import Any
from app.api import schemas
import aiofiles
import toml

from app.config import base_config


class FileWorker(ABC):

    def __init__(self, path_to_file: str) -> None:
        self.__path_to_file = path_to_file

    @abstractmethod
    async def read_file(self) -> Any:
        pass


class TomlWorker(FileWorker):

    def __init__(self, path_to_file: str) -> None:
        super().__init__(path_to_file)
        self.__path_to_file = path_to_file

    async def read_file(self) -> dict:
        async with aiofiles.open(self.__path_to_file, "r") as file:
            file_data = await file.read()
            parsed_toml = toml.loads(file_data)
            return parsed_toml
