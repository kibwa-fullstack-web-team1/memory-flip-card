from pydantic import BaseModel
from datetime import datetime
from pydantic.config import ConfigDict
from typing import Optional, List

class FamilyPhotoBase(BaseModel):
    user_id: str
    file_path: str

class FamilyPhotoCreate(FamilyPhotoBase):
    pass

class FamilyPhoto(FamilyPhotoBase):
    id: int
    upload_time: datetime
    card_image_urls: Optional[List[str]] = None
    
    model_config = ConfigDict(from_attributes=True)

