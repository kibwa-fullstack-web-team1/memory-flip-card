from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.deps.db import get_db
from app.helper.photo_helper import get_user_photos
from app.models.upload_photo import FamilyPhoto
from app.models.card_image import CardImage
from app.schemas.photo_schema import FamilyPhotoListResponse, PhotoItem

router = APIRouter()

# 가족사진 목록 조회 API
@router.get("/family-photos", response_model=FamilyPhotoListResponse)
def get_family_photos(user_id: str = Query(...), db: Session = Depends(get_db)):
    """
    가족 사진 목록 조회 API
    """
    photos = get_user_photos(db, user_id)

    if not photos:
        raise HTTPException(status_code=404, detail="등록된 가족사진이 없습니다.")

    return FamilyPhotoListResponse(
        user_id=user_id,
        photos=[PhotoItem(id=photo.id, file_url=photo.file_path) for photo in photos]
    )

# # 모델 처리된 이미지 목록 조회 API (주석 처리)
# @router.get("/processed-photos", response_model=FamilyPhotoListResponse)
# def get_processed_photos(user_id: str = Query(...), db: Session = Depends(get_db)):
#     photos = get_user_photos(db, user_id)
#
#     if not photos:
#         raise HTTPException(status_code=404, detail="등록된 사진이 없습니다.")
#
#     # 모델 처리된 이미지가 존재하는 것만 필터링
#     processed_photos = [photo for photo in photos if photo.processed_file_path]
#
#     if not processed_photos:
#         raise HTTPException(status_code=404, detail="처리된 이미지가 없습니다.")
#
#     return FamilyPhotoListResponse(
#         user_id=user_id,
#         photos=[PhotoItem(id=photo.id, file_url=photo.processed_file_path) for photo in processed_photos]
#     )

# 사용자별 카드 이미지 목록 조회 API
@router.get("/cards", response_model=List[str])
def get_user_cards(user_id: str, db: Session = Depends(get_db)):
    """
    사용자 카드 이미지 목록 조회 API
    """
    try:
        # CardImage 테이블에서 user_id에 해당하는 모든 카드 조회
        cards = db.query(CardImage).join(FamilyPhoto).filter(FamilyPhoto.user_id == user_id).all()
        
        if not cards:
            raise HTTPException(status_code=404, detail="해당 사용자의 카드 이미지를 찾을 수 없습니다.")
        
        # 카드 URL만 추출하여 리스트로 반환
        card_urls = [card.card_url for card in cards]
        return card_urls
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"카드 이미지 조회 실패: {str(e)}")
