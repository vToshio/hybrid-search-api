from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from typing import List
from os import getenv

load_dotenv()

class EmbeddingsService:
    _model_name = getenv('HF_MODEL')
    _model = SentenceTransformer(_model_name)

    @classmethod
    def generate_embeddings(cls, text: str) -> List[float]:
        return cls._model.encode(text)