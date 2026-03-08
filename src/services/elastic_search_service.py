from config.initializers.elastic_search_client import ElasticsearchClient
from src.services.embedding_service import EmbeddingsService

class ElasticsearchService:
    def __init__(self, index_name: str = 'documents'):
        self.client = ElasticsearchClient.get_client()
        self.index_name = index_name

    def index_document(self, content: dict):
        return self.client.index(
            index=self.index_name,
            document=content,
        )

    # Obs: Verificar a possibilidade de adicionar uma "strategy" para identificar
    # o tipo de pesquisa futuramente, a partir de parametrizações, e manter na API
    # o mesmo endpoint /search para realizar tipos de pesquisas diferentes
    def search(self, query: str) -> dict:
        return self.client.search(
            index=self.index_name,
            query={
                'match': {
                    'content': query
                }
            }
        )

    def fuzzy_search(self, query: str) -> dict:
        return self.client.search(
            index=self.index_name,
            query={
                'match': {
                    'content': {
                        'query': query,
                        'fuzziness': 2,    # pode ser [0, 1, 2]
                        'prefix_length': 1 
                    }
                }
            }
        )

    def hybrid_search(self, query: str):
        query_vector = EmbeddingsService.generate_embeddings(query)

        return self.client.search(
            index=self.index_name,
            size=10,
            query={
                'match': {
                    'content': {
                        'query': query,
                        'fuzziness': 'AUTO',
                        'boost': 0.3
                    }
                }
            },
            knn={
                'field': 'embeddings',
                'query_vector': query_vector,
                'k': 10,
                'num_candidates': 100
            }
        )