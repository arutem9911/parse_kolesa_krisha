from datetime import datetime
from typing import List, Dict, Any
from uuid import UUID

from pydantic import BaseModel


class BaseAdvert(BaseModel):
    task_id: UUID
    advert_ids: List[str] = []
    created_at: datetime = datetime.now()
    data_flats: Dict[dict] = {}
    data_cars: Dict[dict] = {}
