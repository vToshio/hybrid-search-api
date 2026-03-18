from config.initializers.embeddings_model import EmbeddingsModel
from config.settings import settings
from typing import Union, List

class EmbeddingsService:
    _model_name = settings.hf_model
    _model = EmbeddingsModel.get()

    @classmethod
    def generate_embeddings(cls, text: Union[str, List[str]], batch_size: int = 32, is_query:bool = True) -> List[float]:
        prefix: str = 'query: ' if is_query else 'passage: '

        text_with_prefix = ''
        if isinstance(text, str):
            text_with_prefix = f'{prefix}{text}'
        else:
            text_with_prefix = [f'{prefix}{t}' for t in text]

        return cls._model.encode(
            text_with_prefix, 
            batch_size=batch_size, 
            show_progress_bar=False,
            normalize_embeddings=True
        )