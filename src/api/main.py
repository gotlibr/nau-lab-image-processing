from fastapi import FastAPI
from .views.router import router
from src.common.config.settings import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

app.include_router(router, prefix=settings.API_V1_STR)