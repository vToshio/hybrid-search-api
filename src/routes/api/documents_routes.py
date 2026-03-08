from fastapi import APIRouter, UploadFile

from src.schemas.document_schema import DocumentSchema
from src.services.document_service import DocumentService
from src.services.embedding_service import EmbeddingsService
from src.services.elastic_search_service import ElasticsearchService

documents_router = APIRouter(prefix='/documents')
search_engine = ElasticsearchService('documents')

@documents_router.post('/index-content')
async def index_content(document: UploadFile) -> DocumentSchema:
    file = DocumentService(document)
    content = await file.get_file_content()
    embeddings = EmbeddingsService.generate_embeddings(content)
    search_engine.index_document(
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
        embeddings=embeddings
    )

@documents_router.get('/search')
async def search(query: str):
    results = search_engine.search(query)

    hits = [
        hit['_source'] for hit in results['hits']['hits']
    ]

    return hits