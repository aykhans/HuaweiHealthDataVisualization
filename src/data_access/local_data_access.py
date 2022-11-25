from pathlib import Path
from typing import List
import json
from .data_opeartions import DataOperations


class LocalDataAccess(DataOperations):
    def __init__(self, data_folder_name: str) -> None:
        self.data_dir: Path =\
            Path(__file__).resolve().parent.parent.parent / data_folder_name

    @property
    def data(self) -> List:
        return self._data

    @data.setter
    def data(self, file_name: str):
        with open(self.data_dir / file_name) as f:
            self._data = json.load(f)