from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class CardImage(Base):
    __tablename__ = "card_images"
    
    id = Column(Integer, primary_key=True, index=True)
    family_photo_id = Column(Integer, ForeignKey("family_photos.id"), nullable=False)
    card_url = Column(String, nullable=False)
    card_index = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 관계 설정
    family_photo = relationship("FamilyPhoto", back_populates="card_images")