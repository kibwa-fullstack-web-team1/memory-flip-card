from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.deps.db import get_db
from app.models.upload_photo import FamilyPhoto
from app.schemas.photo_schema import FamilyPhotoListResponse, PhotoItem

router = APIRouter()

#가족사진 목록 조회 API
@router.get("/", response_model=FamilyPhotoListResponse)
def get_family_photos(user_id: str = Query(...), db: Session = Depends(get_db)):
    photos = db.query(FamilyPhoto).filter(FamilyPhoto.user_id == user_id).all()

    if not photos:
        raise HTTPException(status_code=404, detail="등록된 가족사진이 없습니다.")

    return FamilyPhotoListResponse(
        user_id=user_id,
        photos=[PhotoItem(id=photo.id, file_url=photo.file_path) for photo in photos]
    )
