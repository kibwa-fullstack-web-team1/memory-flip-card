from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class FamilyPhoto(Base):
    __tablename__ = "family_photos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    file_path = Column(String, nullable=False) # 원본 사진 S3 URL
    upload_time = Column(DateTime, default=datetime.utcnow)
    
   # 관계 설정
    card_images = relationship("CardImage", back_populates="family_photo")