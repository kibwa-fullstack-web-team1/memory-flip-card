from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from typing import Optional

from app.deps.db import get_db
from app.models.upload_photo import FamilyPhoto
from app.models.game_result import GameResult
from app.schemas.photo_schema import FamilyPhotoListResponse, PhotoItem
from app.schemas.record_scehma import GameResultCreate

router = APIRouter()

#게임 결과 저장 API
@router.post("/game")
def save_game_result(
    result: GameResultCreate,
    db: Session = Depends(get_db)
):
    try:
        # 여기에 게임 결과를 저장하는 모델을 생성하고 DB에 저장
        game_result = GameResult(
            user_id=result.user_id,
            score=result.score,
            duration_seconds=result.duration_seconds,  
            attempts=result.attempts,
            matches=result.matches,
            difficulty=result.difficulty
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

