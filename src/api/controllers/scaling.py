# src/api/controllers/scaling.py
from typing import Optional
from ..models.task import TaskCreate, Task
from ..repositories.tasks import TaskRepository
from datetime import datetime
import uuid
import redis.asyncio as redis
from ..models.image import ImageCreate, Image
from src.common.config.settings import settings

class ScalingController:
    def __init__(self):
        self.task_repo = TaskRepository()
        self.redis = redis.from_url(settings.REDIS_URL)

    async def create_task(self, file, width: int, height: int, preserve_ratio: bool) -> Task:
        # Create task
        task_id = str(uuid.uuid4())
        image_data = await file.read()
        
        task = Task(
            id=task_id,
            image_id=file.filename,
            width=width,
            height=height,
            preserve_ratio=preserve_ratio,
            status="pending",
            created_at=datetime.utcnow()
        )
        
        # Save task
        created_task = await self.task_repo.create(task)
        
        # Store image data temporarily
        await self.redis.set(f'image:{task_id}', image_data)
        
        # Add to processing queue
        await self.redis.lpush('image_scaling:queue', task.model_dump_json())
        
        return created_task

    async def get_task(self, task_id: str) -> Optional[Task]:
        return await self.task_repo.get(task_id)

    async def get_result(self, task_id: str) -> dict:
        task = await self.get_task(task_id)
        if not task:
            return {"status": "not_found"}
            
        if task.status != "completed":
            return {"status": task.status}
        
        result = await self.redis.get(f'result:{task_id}')
        return {
            "status": "completed",
            "data": result.decode('utf-8') if result else None
        }