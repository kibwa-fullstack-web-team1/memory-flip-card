from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional, List

from app.deps.db import get_db
from app.models.upload_photo import FamilyPhoto
from app.models.game_result import GameResult
from app.schemas.photo_schema import FamilyPhotoListResponse, PhotoItem
from app.schemas.record_schema import GameResultCreate, GameResultResponse, GameResultListResponse

router = APIRouter()

#게임 결과 저장 API
@router.post("/records")
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

#게임 결과 조회 API
@router.get("/list", response_model=GameResultListResponse)
def get_game_results(
    user_id: str = Query(..., description="사용자 ID"),
    limit: int = Query(10, description="조회할 결과 수", ge=1, le=100),
    offset: int = Query(0, description="건너뛸 결과 수", ge=0),
    db: Session = Depends(get_db)
):
    try:
        # 사용자 ID로 게임 결과 조회 (최신순으로 정렬)
        results = db.query(GameResult).filter(
            GameResult.user_id == user_id
        ).order_by(
            desc(GameResult.id)  # 최신 결과가 먼저 오도록 정렬
        ).offset(offset).limit(limit).all()
        
        if not results:
            return GameResultListResponse(
                user_id=user_id,
                count=0,
                results=[]
            )
        
        return GameResultListResponse(
            user_id=user_id,
            count=len(results),
            results=[
                GameResultResponse(
                    id=result.id,
                    score=result.score,
                    attempts=result.attempts,
                    matches=result.matches,
                    duration_seconds=result.duration_seconds,
                    difficulty=result.difficulty
                ) for result in results
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"게임 결과 조회 실패: {str(e)}")