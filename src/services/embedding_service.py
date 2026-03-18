from config.initializers.embeddings_model import EmbeddingsModel
from config.settings import settings
from typing import List

class EmbeddingsService:
    _model_name = settings.hf_model
    _model = EmbeddingsModel.get()

    @classmethod
    def generate_embeddings(cls, text: List[str], batch_size: int = 32) -> List[float]:
        return cls._model.encode(text, batch_size=batch_size, show_progress_bar=False)