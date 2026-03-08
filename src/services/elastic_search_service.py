from config.initializers.elastic_search_client import ElasticsearchClient
from elasticsearch import Elasticsearch

class ElasticsearchService:
    def __init__(self, index_name: str = 'documents'):
        self.client = ElasticsearchClient.get_client()
        self.index_name = index_name

    def index_document(self, content: dict):
        return self.client.index(
            index=self.index_name,
            document=content,
        )
    
    def search(self, query: str):
        return self.client.search(
            index=self.index_name,
            query={
                'match': {
                    'content': query
                }
            }
        )