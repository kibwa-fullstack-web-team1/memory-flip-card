from pydantic import BaseModel, HttpUrl
from typing import List

class PhotoItem(BaseModel):
    id: int
    file_url: HttpUrl

    class Config:
        orm_mode = True

class FamilyPhotoListResponse(BaseModel):
    user_id: str
    photos: List[PhotoItem]
