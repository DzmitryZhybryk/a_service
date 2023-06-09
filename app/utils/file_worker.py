"""Module for storage FileWorker classes"""
from abc import ABC, abstractmethod
from typing import Any

import aiofiles
import toml


class FileWorker(ABC):
    """
    Abstract class, implements contracts for child classes

    Args:
        path_to_file: path for working file

    """

    def __init__(self, path_to_file: str) -> None:
        self.__path_to_file = path_to_file

    @abstractmethod
    async def read_file(self) -> Any:
        pass


class TomlWorker(FileWorker):
    """
    Class for work with .toml files

    Args:
        path_to_file: path for working file

    """

    def __init__(self, path_to_file: str) -> None:
        super().__init__(path_to_file)
        self.__path_to_file = path_to_file

    async def read_file(self) -> dict:
        """
        Method read file

        Returns:
            dict with data from file

        """
        async with aiofiles.open(self.__path_to_file, "r") as file:
            file_data = await file.read()
            parsed_toml = toml.loads(file_data)
            return parsed_toml
