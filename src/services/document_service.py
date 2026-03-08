from fastapi import UploadFile
from os.path import splitext

from src.services.extraction.pdf_extractor import PDFExtractor
from src.services.extraction.extraction_factory import ExtractionFactory

class DocumentService:
    def __init__(self, document: UploadFile):
        self._document = document
        self.name = document.filename
        self.extension = self._get_file_extension()
        self._extraction_strategy = ExtractionFactory.create(self.extension)

    async def get_file_content(self) -> str:
        return await self._extraction_strategy.extract_content(self._document)
  
    def _get_file_extension(self) -> str:
        return splitext(self.name)[1].lstrip('.')
