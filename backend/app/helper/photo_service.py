from fastapi import UploadFile, HTTPException
import uuid
from datetime import datetime
from app.core.config import get_s3_client, get_settings
from app.models.upload_photo import FamilyPhoto

def upload_photo_to_s3(file: UploadFile, user_id: str) -> str:
    """
    S3에 사진을 업로드하고 URL을 반환합니다.
    
    Args:
        file: 업로드할 파일
        user_id: 사용자 ID
        
    Returns:
        str: 업로드된 파일의 S3 URL
    """

    # 파일 유효성 검사
    if not file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        raise HTTPException(status_code=400, detail="이미지 파일만 허용됩니다.")
    
    # S3 업로드
    return upload_file_to_s3(file, user_id, "family_photos")

def save_photo_record(db: Session, user_id: str, file_url: str) -> FamilyPhoto:
    """
    사진 정보를 데이터베이스에 저장합니다.
    
    Args:
        db: 데이터베이스 세션
        user_id: 사용자 ID
        file_url: 파일 URL
        
    Returns:
        FamilyPhoto: 저장된 사진 레코드
    """
    photo_record = FamilyPhoto(
        user_id=user_id,
        file_path=file_url
    )
    db.add(photo_record)
    db.commit()
    db.refresh(photo_record)
    return photo_record
    
def get_user_photos(db: Session, user_id: str) -> list[FamilyPhoto]:
    """
    사용자의 모든 사진을 조회합니다.
    
    Args:
        db: 데이터베이스 세션
        user_id: 사용자 ID
        
    Returns:
        list[FamilyPhoto]: 사용자의 사진 목록
    """
    return db.query(FamilyPhoto).filter(FamilyPhoto.user_id == user_id).all()