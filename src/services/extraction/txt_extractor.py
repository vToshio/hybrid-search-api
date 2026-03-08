from src.services.extraction.base_extraction_service import BaseExtractionService
from fastapi import UploadFile
from typing import List

class TXTExtractor(BaseExtractionService):
    @staticmethod
    async def extract_content(file: UploadFile) -> str | List[dict]:
        return await file.read()