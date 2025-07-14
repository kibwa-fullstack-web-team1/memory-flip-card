from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from typing import Optional

from app.deps.db import get_db
from app.models.upload_photo import FamilyPhoto
from app.schemas.photo_schema import FamilyPhotoListResponse, PhotoItem

router = APIRouter()

#게임 결과 저장 API
@router.post("/")
def save_game_result(
    user_id: str = Body(...),
    score: int = Body(...),
    play_time: int = Body(...),
    difficulty: Optional[str] = Body(None),
    db: Session = Depends(get_db)
):
    try:
        # 여기에 게임 결과를 저장하는 모델을 생성하고 DB에 저장
        game_result = GameResult(
            user_id=user_id,
            score=score,
            play_time=play_time,
            difficulty=difficulty
        )
        
        db.add(game_result)
        db.commit()
        db.refresh(game_result)
        
        return {
            "success": True,
            "message": "게임 결과가 성공적으로 저장되었습니다.",
            "result_id": game_result.id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"게임 결과 저장 실패: {str(e)}")
