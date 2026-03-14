from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from os import getenv

load_dotenv()

class EmbeddingsModel:
    _instance: SentenceTransformer | None = None

    @classmethod
    def get(cls) -> SentenceTransformer:
        if cls._instance is None:
            cls._instance = SentenceTransformer(getenv('HF_MODEL'))
        return cls._instance