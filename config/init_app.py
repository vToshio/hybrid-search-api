from fastapi import FastAPI

from src.routes.hello_routes import hello_router
from src.routes.api.documents_routes import documents_router

def init_app(debug: bool = False, ) -> FastAPI:
    '''Instância a aplicação com as configurações básicas.'''
    app = FastAPI(
        title="Pesquisa de Documentos com ElasticSearch",
        summary='Protótipo de pesquisa de documentos utilizando Pesquisa Híbrida com o ElasticSearch',
        debug=bool(debug)
    )
    
    app.include_router(hello_router, prefix='/api')
    app.include_router(documents_router, prefix='/api')

    return app