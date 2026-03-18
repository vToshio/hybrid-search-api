from fastapi import APIRouter, UploadFile, Depends, BackgroundTasks

from src.services.document_service import DocumentService
from src.services.chunk_service import ChunkService
from src.services.embedding_service import EmbeddingsService
from src.services.elastic_search_service import ElasticsearchService
from src.dependencies.elasticsearch import get_es_service

import time

documents_router = APIRouter(prefix='/documents')

async def process_and_index(text: str, doc_name: str, search_engine: ElasticsearchService):
    chunks = ChunkService.split(text)
    texts = [chunk.page_content for chunk in chunks]

    embeddings_list = EmbeddingsService.generate_embeddings(texts, is_query=False)
    
    bulk_data = []
    for index, (txt, emb) in enumerate(zip(texts, embeddings_list)):
        bulk_data.append({
            'content': txt,
            'embeddings': emb.tolist(),
            'document_name': doc_name,
            'chunk_id': index
        })

    await search_engine.bulk_index_documents(bulk_data)

@documents_router.post('/store')
async def index_content(
    document: UploadFile, 
    background_tasks: BackgroundTasks,
    search_engine = Depends(get_es_service)
) -> dict:
    start = time.time()

    file = DocumentService(document)
    raw = await file.get_file_content()

    background_tasks.add_task(
        process_and_index,
        raw,
        file.name,
        search_engine
    )
    
    return {
        'document_name': file.name,
        'status': 'Processado',
        'elapsed_time': time.time() - start
    }

@documents_router.delete('/recreate-index')
async def recreate_index(search_engine = Depends(get_es_service)):
    return await search_engine.recreate_index()


@documents_router.get('/search')
async def search(query: str, search_engine = Depends(get_es_service)):
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

@documents_router.get('/hybrid-search')
async def hybrid_search(query: str, search_engine=Depends(get_es_service)):
    start = time.time()
    results = await search_engine.hybrid_search(query)
    end = time.time()

    hits = [{
        'document_name': hit['_source'].get('document_name'),
        'chunk_id': hit['_source'].get('chunk_id'),
        'score': hit['_score'],
        'content': hit['_source'].get('content')
    } for hit in results['hits']['hits']]

    processed_inner_hits = []
    for doc_hit in results['hits']['hits']:
        inner_hits_data = doc_hit.get('inner_hits', {}).get('best_scores', {}).get('hits', {}).get('hits', {})

        for chunk_hit in inner_hits_data:
            processed_inner_hits.append({
                'document_name': doc_hit['_source'].get('document_name'),
                'chunk_id': chunk_hit['_source'].get('chunk_id'),
                'score': chunk_hit['_score'],
                'content': chunk_hit['_source'].get('content'),
            })

    return {
        'elapsed_time': end - start,
        'hits': hits,
        'inner_hits': processed_inner_hits
    }