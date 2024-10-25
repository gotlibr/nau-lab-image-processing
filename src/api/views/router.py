from fastapi import APIRouter, File, UploadFile, Depends
from ..controllers.scaling import ScalingController
from ..models.task import TaskCreate

router = APIRouter()
scaling_controller = ScalingController()

@router.post("/tasks")
async def create_task(
    file: UploadFile = File(...),
    width: int = 800,
    height: int = 600,
    preserve_ratio: bool = True
):
    return await scaling_controller.create_task(file, width, height, preserve_ratio)

@router.get("/tasks/{task_id}")
async def get_task(task_id: str):
    return await scaling_controller.get_task(task_id)

@router.get("/results/{task_id}")
async def get_result(task_id: str):
    return await scaling_controller.get_result(task_id)
