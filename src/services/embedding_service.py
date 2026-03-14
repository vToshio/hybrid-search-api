from config.initializers.embeddings_model import EmbeddingsModel

from dotenv import load_dotenv
from typing import List
from os import getenv

load_dotenv()

class EmbeddingsService:
    _model_name = getenv('HF_MODEL')
    _model = EmbeddingsModel.get()

    @classmethod
    def generate_embeddings(cls, text: str) -> List[float]:
        return cls._model.encode(text)