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
        
        return cls._client