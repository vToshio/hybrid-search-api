from src.services.extraction.base_extraction_service import BaseExtractionService
from fastapi import UploadFile
from typing import List
import pymupdf4llm
import fitz

class PDFExtractor(BaseExtractionService):
    @staticmethod
    async def extract_content(file: UploadFile) -> str | List[dict]:
        doc_bytes = await file.read()
        content = fitz.open(stream=doc_bytes, filetype='pdf')

        return pymupdf4llm.to_markdown(content)
        