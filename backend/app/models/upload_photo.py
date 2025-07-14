from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base
from datetime import datetime


class FamilyPhoto(Base):
    __tablename__ = "family_photos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    upload_time = Column(DateTime, default=datetime.utcnow)
