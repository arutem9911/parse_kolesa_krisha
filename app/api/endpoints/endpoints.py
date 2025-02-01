import dotenv
from fastapi import APIRouter
from starlette import status

from app.error_handler.error_handler import try_execute_async
from app.service.base_service import base_service
from app.settings.config import settings

router = APIRouter()
dotenv.load_dotenv()

tasks: dict = {}


@router.get("/health")
async def test_api():
    return {"status_code": status.HTTP_200_OK}


@router.post("/start-collection/")
@try_execute_async
async def start_collection(collection=settings.MONGO_COLLECT):
    await base_service()
