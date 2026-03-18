from pydantic import BaseModel
from typing import List

class ChunkSchema(BaseModel): 
    chunk_id: int
    content: str
    embeddings: List[float]