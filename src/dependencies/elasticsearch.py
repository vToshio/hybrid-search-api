from fastapi import Request, Depends
from src.services.elastic_search_service import ElasticsearchService

def get_es_service(request: Request):
    return ElasticsearchService(client=request.app.state.elasticsearch)
