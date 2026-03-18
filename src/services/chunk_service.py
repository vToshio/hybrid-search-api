from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List

class ChunkService:
    _splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    @classmethod
    def split(cls, text: str) -> List[str]:
        return cls._splitter.create_documents([text])