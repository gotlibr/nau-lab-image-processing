# src/processor/services/processor.py
from PIL import Image
import io
from ..models.task import ProcessingTask
import redis.asyncio as redis
import json
from src.common.config.settings import settings

class ImageProcessor:
    def __init__(self):
        self.redis = redis.from_url(settings.REDIS_URL)

    async def process_image(self, image_data: bytes, task: ProcessingTask) -> bytes:
        img = Image.open(io.BytesIO(image_data))
        
        if task.preserve_ratio:
            ratio = min(task.width/img.width, task.height/img.height)
            new_size = (int(img.width * ratio), int(img.height * ratio))
        else:
            new_size = (task.width, task.height)
            
        scaled_img = img.resize(new_size, Image.LANCZOS)
        
        output = io.BytesIO()
        scaled_img.save(output, format=img.format or 'JPEG')
        return output.getvalue()

    async def process_task(self, task_json: str):
        task = ProcessingTask.parse_raw(task_json)
        try:
            # Get image data (implementation depends on your storage solution)
            image_data = await self.get_image_data(task.image_id)
            
            # Process image
            result = await self.process_image(image_data, task)
            
            # Save result
            await self.redis.set(f'result:{task.id}', result)
            await self.update_task_status(task.id, "completed")
        except Exception as e:
            print(f"Error processing task {task.id}: {str(e)}")
            await self.update_task_status(task.id, "error")

    async def get_image_data(self, image_id: str) -> bytes:
        # Implementation depends on your storage solution
        # This is a placeholder
        return b''

    async def update_task_status(self, task_id: str, status: str):
        # Implementation with your database
        await self.redis.set(f'status:{task_id}', status)