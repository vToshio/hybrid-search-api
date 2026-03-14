from fastapi import FastAPI
from contextlib import asynccontextmanager
from elasticsearch import AsyncElasticsearch
from config.elasticsearch.indexes_config import documents_index_body

from src.routes.hello_routes import hello_router
from src.routes.api.documents_routes import documents_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    es = AsyncElasticsearch('http://elasticsearch:9200')
    app.state.elasticsearch = es

    if not await es.indices.exists(index='documents'):
        try:
            await es.indices.create(
                index='documents',
                body=documents_index_body
            )
        except ConnectionError as e:
            print(f'[ELASTICSEARCH CONNECTION ERROR]: {str(e)}')

    yield

    await es.close()

def init_app(debug: bool = False, ) -> FastAPI:
    '''Instância a aplicação com as configurações básicas.'''
    app = FastAPI(
        title="Pesquisa de Documentos com ElasticSearch",
        summary='Protótipo de pesquisa de documentos utilizando Pesquisa Híbrida com o ElasticSearch',
        debug=bool(debug),
        lifespan=lifespan
    )
    
    app.include_router(hello_router, prefix='/api')
    app.include_router(documents_router, prefix='/api')

    return app