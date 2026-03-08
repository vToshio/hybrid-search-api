from fastapi import APIRouter, UploadFile

from src.schemas.document_schema import DocumentSchema
from src.services.document_service import DocumentService

documents_router = APIRouter(prefix='/documents')

@documents_router.post('/index-content')
async def index_content(document: UploadFile) -> DocumentSchema:
    file = DocumentService(document)

    return DocumentSchema(
        name=file.name,
        extension=file.extension,
        content=await file.get_file_content()
    )