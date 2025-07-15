from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.deps.db import get_db
from app.helper.photo_service import get_user_photos
from app.models.upload_photo import FamilyPhoto
from app.schemas.photo_schema import FamilyPhotoListResponse, PhotoItem

router = APIRouter()

#가족사진 목록 조회 API
@router.get("/family-photos", response_model=FamilyPhotoListResponse)
def get_family_photos(user_id: str = Query(...), db: Session = Depends(get_db)):
    photos = get_user_photos(db, user_id)

    if not photos:
        raise HTTPException(status_code=404, detail="등록된 가족사진이 없습니다.")

    return FamilyPhotoListResponse(
        user_id=user_id,
        photos=[PhotoItem(id=photo.id, file_url=photo.file_path) for photo in photos]
    )
