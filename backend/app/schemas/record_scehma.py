from pydantic import BaseModel
from typing import Optional

class GameResultCreate(BaseModel):
    user_id: str
    score: int
    attempts: int
    matches: int
    duration_seconds: int
    difficulty: Optional[str] = None
