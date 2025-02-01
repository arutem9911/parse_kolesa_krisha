import traceback
import uuid
from functools import wraps

from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError
from starlette import status
from starlette.responses import JSONResponse

from app.schemas.response_data import ResponseData
from app.settings.mongo_db import insert_application_data


def try_execute_async(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        collection = kwargs.get("collection", None)
        kwargs.get("http_client", None)
        try:
            response_data = await func(*args, **kwargs)
            # insert_application_data(response_data.dict(), status.HTTP_200_OK, collection)
            return response_data
        except Exception as e:
            error = False
            task_id = str(uuid.uuid4())
            if isinstance(e, ValidationError):
                error = e
            if isinstance(e, RequestErrorBadRequest):
                error = e.message  # type: ignore
            if not error:
                error = traceback.format_exc()  # type: ignore
            data = {
                "status": "Cancelled",
                "message": error,
                "task_id": task_id,
            }
            response = ResponseData.model_validate(data)
            insert_application_data(response.dict(), status.HTTP_400_BAD_REQUEST, collection)
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=jsonable_encoder(response),
            )

    return wrapper


class RequestError(Exception):
    def __init__(self, message: str, code: int) -> None:
        self.message = message
        self.code = code

    def __str__(self):
        return self.message


class RequestErrorNotFound(RequestError):
    def __init__(self, message, code=404):
        super().__init__(message=message, code=code)
        self.code = code


class RequestErrorBadRequest(RequestError):
    def __init__(self, message, code=400):
        super().__init__(message=message, code=code)
        self.code = code


class RequestErrorServerError(RequestError):
    def __init__(self, message, code=500):
        super().__init__(message=message, code=code)
        self.code = code
