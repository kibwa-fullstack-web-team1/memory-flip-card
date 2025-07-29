from sqlalchemy import Column, Integer, String, DateTime, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class FamilyPhoto(Base):
    __tablename__ = "family_photos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    file_path = Column(String, nullable=False) # 원본 사진 S3 URL
    processed_file_path = Column(String, nullable=True) # 이미지 처리된 사진 S3 URL
    file_hash = Column(String, nullable=True) # 해시값으로 중복 체크
    upload_time = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint('user_id', 'file_hash', name='user_file_hash_uc'),)
    
   # 관계 설정
    card_images = relationship("CardImage", back_populates="family_photo")