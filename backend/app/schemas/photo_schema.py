from pydantic import BaseModel, HttpUrl, ConfigDict
from typing import List

class PhotoItem(BaseModel):
    id: int
    file_url: HttpUrl

    model_config = ConfigDict(from_attributes=True)

class FamilyPhotoListResponse(BaseModel):
    user_id: str
    photos: List[PhotoItem]
