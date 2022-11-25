import json
from typing import List
from streamlit.runtime.uploaded_file_manager import UploadedFile
from .data_opeartions import DataOperations


class UploadDataAccess(DataOperations):
    def __init__(self) -> None:
        super().__init__()

    @property
    def data(self) -> List:
        return self._data

    @data.setter
    def data(self, uploaded_file: UploadedFile) -> None:
        self._data = json.load(uploaded_file)