from pathlib import Path
import json
from typing import List
from .data_opeartions import DataOperations


class LocalDataAccess(DataOperations):
    def __init__(self, data_folder_name: str) -> None:
        self.data = None
        self.data_dir: Path =\
            Path(__file__).resolve().parent.parent.parent / data_folder_name

    def get_data(self, file_name: str) -> List:
        with open(self.data_dir / file_name) as f:
            self.data: List = json.load(f)
        return self.data