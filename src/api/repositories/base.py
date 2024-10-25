# src/api/repositories/base.py
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self):
        pass

    async def get(self, id: Any) -> Optional[ModelType]:
        raise NotImplementedError

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        raise NotImplementedError