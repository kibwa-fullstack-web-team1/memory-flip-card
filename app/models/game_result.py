from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base
from datetime import datetime

class GameResult(Base):
    __tablename__ = "game_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    score = Column(Integer, nullable=False) # =matches
    attempts = Column(Integer, nullable=False)
    matches = Column(Integer, nullable=False)
    duration_seconds = Column(Integer, nullable=False)
    difficulty = Column(String, nullable=True)
