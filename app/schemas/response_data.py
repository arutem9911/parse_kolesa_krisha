from uuid import UUID

from pydantic import BaseModel


class ResponseData(BaseModel):
    status: str = "in_progress"
    message: str | None = None
    task_id: UUID
