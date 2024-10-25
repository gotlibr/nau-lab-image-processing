from pydantic import BaseModel

class ImageBase(BaseModel):
    content_type: str
    size: int

class ImageCreate(ImageBase):
    data: bytes

class Image(ImageBase):
    id: str
    url: str
