from elasticsearch import Elasticsearch
from dotenv import load_dotenv
from os import getenv

load_dotenv()

class ElasticsearchClient:
    _client: Elasticsearch | None = None

    @classmethod
    def get_client(cls) -> Elasticsearch:
        if cls._client is None:
            cls._client = Elasticsearch(
                getenv('ELASTIC_URL', 'http://elasticsearch:9200')
            )
            if not cls._client.indices.exists(index='documents'): 
                cls._create_indexes('documents')
        
        return cls._client
    
    @classmethod
    def _create_indexes(cls, index_name: str = 'documents'):
        cls._client.indices.create(
            index=index_name, 
            body=cls._documents_body()
        )

    @staticmethod
    def _documents_body() -> dict:
        return {
            'settings': {
                'number_of_shards': getenv('ES_SHARDS_NUMBER', 1),
                'number_of_replicas': getenv('ES_REPLICAS_NUMBER', 0)
            },
            'mappings': {
                'properties': {
                    'name': { 'type': 'text' },
                    'content': { 'type': 'text' },
                    'embeddings': { 
                        'type': 'dense_vector', # Vetor Denso VS Vetor Esparso?
                        'dims': 768,            # Dimensionamento dos embeddings -> definido pelo modelo de embeddings
                        'index': True,
                        'similarity': 'cosine' 
                    }
                }
            }
        }