from abc import ABC
from fastapi import UploadFile
from typing import List

class BaseExtractionService(ABC):
    @staticmethod
    def extract_content(file: UploadFile) -> str | List[dict]:
        raise NotImplementedError