from typing import Optional
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.s3_service import upload_pil_image_to_s3
from app.config.config import get_s3_client, get_settings
from app.models.upload_photo import FamilyPhoto

def save_photo_record(db: Session, user_id: str, file_url: str, file_hash: str) -> FamilyPhoto:
    """
    원본 사진 정보를 데이터베이스에 저장합니다.
    
    Args:
        db: 데이터베이스 세션
        user_id: 사용자 ID
        file_url: 파일 URL
        file_hash: 파일 해시
        
    Returns:
        FamilyPhoto: 저장된 사진 레코드
    """
    photo_record = FamilyPhoto(
        user_id=user_id,
        file_path=file_url,
        file_hash=file_hash,
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

def get_processed_photos(db: Session, user_id: str) -> list[FamilyPhoto]:
    """
    처리된 이미지만 필터링하여 조회합니다.
    """
    return (
        db.query(FamilyPhoto)
        .filter(
            FamilyPhoto.user_id == user_id,
            FamilyPhoto.processed_file_path.isnot(None)
        )
        .all()
    )

# 업로드 이미지 중복체크 함수
def check_photo_duplicate(db: Session, user_id: str, file_hash: str) -> Optional[FamilyPhoto]:
    return db.query(FamilyPhoto).filter_by(user_id=user_id, file_hash=file_hash).first()