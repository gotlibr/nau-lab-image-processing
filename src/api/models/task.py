from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    image_id: str
    width: int = Field(gt=0, le=5000)
    height: int = Field(gt=0, le=5000)
    preserve_ratio: bool = True

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
