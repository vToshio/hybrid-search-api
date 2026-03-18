from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from src.services.embedding_service import EmbeddingsService
from config.elasticsearch.indexes_config import *

from typing import List

class ElasticsearchService:
    def __init__(self, client: AsyncElasticsearch, index_name: str = 'documents'):
        self.client = client
        self.index_name = index_name

    async def bulk_index_documents(self, documents: List[dict]):
        actions = [
            {
                '_index': self.index_name,
                '_source': doc
            } for doc in documents
        ]

        await async_bulk(self.client, actions)
    
    async def recreate_index(self):
        if await self.client.indices.exists(index=self.index_name):
            await self.client.options(ignore_status=[400, 404]).indices.delete(index=self.index_name)
        
        response = await self.client.indices.create(
            index=self.index_name,
            body=documents_index_body_v2
        )

        return {
            'index_name': self.index_name,
            'body': response.body
        }

    # Obs: Verificar a possibilidade de adicionar uma "strategy" para identificar
    # o tipo de pesquisa futuramente, a partir de parametrizações, e manter na API
    # o mesmo endpoint /search para realizar tipos de pesquisas diferentes
    async def search(self, query: str) -> dict:
        return await self.client.search(
            index=self.index_name,
            query={
                'match': {
                    'content': {
                        'query': query,
                        'fuzziness': 'AUTO',
                        'prefix_length': 1,
                        'boost': 0.3
                    }
                }
            }
        )

    async def hybrid_search(self, query: str):
        query_vector = EmbeddingsService.generate_embeddings(query)

        return await self.client.search(
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
            },
            collapse={
                'field': 'document_name',
                'inner_hits': {
                    'name': 'best_scores',
                    'size': 5,
                    'sort': [ { '_score': 'desc' } ]
                }
            }
        )