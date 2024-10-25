# src/api/repositories/tasks.py
from typing import Optional
from .base import BaseRepository
from ..models.task import Task, TaskCreate
import redis.asyncio as redis
from src.common.config.settings import settings

class TaskRepository(BaseRepository[Task, TaskCreate, Task]):
    def __init__(self):
        super().__init__()
        self.redis = redis.from_url(settings.REDIS_URL)
        self._tasks = {}  # In-memory storage for demo

    async def get(self, task_id: str) -> Optional[Task]:
        # For demo, we're using in-memory storage
        task = self._tasks.get(task_id)
        if task:
            # Check Redis for updated status
            status = await self.redis.get(f'status:{task_id}')
            if status:
                task.status = status.decode('utf-8')
        return task

    async def create(self, task: Task) -> Task:
        # For demo, store in memory
        self._tasks[task.id] = task
        # Set initial status in Redis
        await self.redis.set(f'status:{task.id}', task.status)
        return task

    async def update(self, task_id: str, update_data: dict) -> Optional[Task]:
        task = self._tasks.get(task_id)
        if task:
            for key, value in update_data.items():
                setattr(task, key, value)
            await self.redis.set(f'status:{task_id}', task.status)
        return task