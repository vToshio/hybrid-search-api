from sentence_transformers import SentenceTransformer
from config.settings import settings
class EmbeddingsModel:
    _instance: SentenceTransformer | None = None

    @classmethod
    def get(cls) -> SentenceTransformer:
        if cls._instance is None:
            cls._instance = SentenceTransformer(settings.hf_model)
        return cls._instance