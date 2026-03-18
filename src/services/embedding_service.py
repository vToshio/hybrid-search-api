from config.initializers.embeddings_model import EmbeddingsModel

from dotenv import load_dotenv
from typing import List
from os import getenv

load_dotenv()

class EmbeddingsService:
    _model_name = getenv('HF_MODEL')
    _model = EmbeddingsModel.get()

    @classmethod
    def generate_embeddings(cls, text: List[str], batch_size: int = 32) -> List[float]:
        return cls._model.encode(text, batch_size=batch_size, show_progress_bar=False)