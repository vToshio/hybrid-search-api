from .base_extraction_service import BaseExtractionService
from .pdf_extractor import PDFExtractor
from .txt_extractor import TXTExtractor

class ExtractionFactory:
    _strategies = {
        'pdf': PDFExtractor,
        'txt': TXTExtractor
    }

    @classmethod
    def create(cls, extension: str) -> BaseExtractionService:
        strategy = cls._strategies.get(extension)

        if not strategy: raise ValueError('Unsupported file extension: ', extension)

        return strategy