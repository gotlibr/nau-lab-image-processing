# src/processor/main.py
import asyncio
import redis.asyncio as redis
from .services.processor import ImageProcessor
from src.common.config.settings import settings

async def main():
    redis_client = redis.from_url(settings.REDIS_URL)
    processor = ImageProcessor()
    
    while True:
        try:
            # Get task from queue
            result = await redis_client.brpop('image_scaling:queue', timeout=0)
            if result:
                _, task_json = result
                # Process task
                await processor.process_task(task_json.decode('utf-8'))
            
        except Exception as e:
            print(f"Error processing task: {e}")
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())