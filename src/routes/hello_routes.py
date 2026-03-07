from fastapi import APIRouter
from ..controllers.hello_controller import HelloController

hello_router = APIRouter()

@hello_router.get('/hello', summary="Retorna uma string Hello World")
async def hello() -> dict:
    return { 'msg': HelloController.hello() }