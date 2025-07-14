from pydantic import BaseModel, HttpUrl
from datetime import datetime
from pydantic.config import ConfigDict

class FamilyPhotoBase(BaseModel):
    user_id: str
    file_path: str

class FamilyPhotoCreate(FamilyPhotoBase):
    pass

class FamilyPhoto(FamilyPhotoBase):
    id: int
    upload_time: datetime

    model_config = ConfigDict(from_attributes=True)
