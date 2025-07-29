from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List

class CardImageBase(BaseModel):
    card_url: str
    card_index: int

class CardImageCreate(CardImageBase):
    family_photo_id: int

class CardImage(CardImageBase):
    id: int
    family_photo_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class FamilyPhotoWithCards(BaseModel):
    id: int
    user_id: str
    file_path: str
    upload_time: datetime
    card_images: List[CardImage] = []
    
    model_config = ConfigDict(from_attributes=True)