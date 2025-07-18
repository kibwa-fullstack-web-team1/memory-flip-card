from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class GameResultCreate(BaseModel):
    user_id: str
    score: int
    attempts: int
    matches: int
    duration_seconds: int
    difficulty: Optional[str] = None

class GameResultResponse(BaseModel):
    id: int
    score: int
    attempts: int
    matches: int
    duration_seconds: int
    difficulty: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class GameResultListResponse(BaseModel):
    user_id: str
    count: int
    results: List[GameResultResponse]