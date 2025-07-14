from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from app.deps.db import get_db
from app.models.upload_photo import FamilyPhoto
from app.helper.photo_service import upload_photo_to_s3

router = APIRouter()

@router.post("/")
async def upload_family_photo(
    user_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 유효성 검사
    if not file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        raise HTTPException(status_code=400, detail="이미지 파일만 허용됩니다.")

    # S3 업로드 서비스 호출
    try:
        s3_url = upload_photo_to_s3(file, user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"S3 업로드 실패: {str(e)}")

    # DB 저장
    photo_record = FamilyPhoto(
        user_id=user_id,
        file_path=s3_url
    )
    db.add(photo_record)
    db.commit()
    db.refresh(photo_record)

    return JSONResponse(status_code=200, content={
        "message": "업로드 성공",
        "photo_id": photo_record.id,
        "file_url": s3_url
    })

# +) 업로드 파일 용량 제한 기능 추가
