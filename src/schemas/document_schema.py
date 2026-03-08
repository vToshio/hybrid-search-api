from pydantic import BaseModel
from typing import List

class DocumentSchema(BaseModel):
    name: str
    extension: str
    content: str | List[dict]
    embeddings: List[float]