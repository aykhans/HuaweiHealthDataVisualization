from pathlib import Path
import json
from typing import List


class LocalTestData:
    def __init__(self, data_folder_name: str) -> None:
        self.data_dir: Path = Path(__file__).resolve().parent.parent.parent / data_folder_name

    def get_data(self, file_name: str) -> List:
        with open(self.data_dir / file_name) as f:
            data: List = json.load(f)
        return data