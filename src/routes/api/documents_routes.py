from fastapi import APIRouter, UploadFile, Depends

from src.schemas.document_schema import DocumentSchema
from src.services.document_service import DocumentService
from src.services.embedding_service import EmbeddingsService
from src.dependencies.elasticsearch import get_es_service

import time

documents_router = APIRouter(prefix='/documents')

@documents_router.post('/index-content')
async def index_content(document: UploadFile, search_engine = Depends(get_es_service)) -> DocumentSchema:
    start = time.time()
    file = DocumentService(document)
    content = await file.get_file_content()
    embeddings = EmbeddingsService.generate_embeddings(content)
    await search_engine.index_document(
        content={
            'name': file.name,
            'content': content,
            'embeddings': embeddings
        }
    )
    
    return DocumentSchema(
        name=file.name,
        extension=file.extension,
        content=content,
        embeddings=embeddings,
        elapsed_time= time.time() - start
    )

@documents_router.get('/simple-search')
async def simple_search(query: str, search_engine = Depends(get_es_service)):
    start = time.time()
    results = await search_engine.search(query)
    end = time.time()

    hits = {
        'elapsed_time': end - start,
        'hits': [
            hit['_source'] for hit in results['hits']['hits']
        ]
    } 
    
    return hits

@documents_router.get('/fuzzy-optimized-search')
async def optimized_search(query: str, search_engine = Depends(get_es_service)):
    start = time.time()
    results = await search_engine.fuzzy_search(query)
    end = time.time()

    hits = {
        'elapsed_time': end - start,
        'hits': [
            hit['_source'] for hit in results['hits']['hits']
        ]
    } 
    
    return hits

@documents_router.get('/hybrid-search')
async def hybrid_search(query: str, search_engine=Depends(get_es_service)):
    start = time.time()
    results = await search_engine.hybrid_search(query)
    end = time.time()

    hits = {
        'elapsed_time': end - start, 
        'hits': [
            { 
            'index': hit['_index'],
            'score': hit['_score'],
            'source': hit['_source']
            } for hit in results['hits']['hits']
        ]
    }

    return hits