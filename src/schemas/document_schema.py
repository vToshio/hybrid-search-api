from pydantic import BaseModel
from typing import List

from src.schemas.chunk_schema import ChunkSchema

class DocumentSchema(BaseModel):
    document_name: str
    extension: str
    chunks: List[ChunkSchema]
    elapsed_time: float
