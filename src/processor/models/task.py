from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProcessingTask(BaseModel):
    id: str
    image_id: str
    width: int
    height: int
    preserve_ratio: bool
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
