from fastapi import UploadFile, HTTPException
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.s3_service import upload_file_to_s3
from app.config.config import get_s3_client, get_settings
from app.models.upload_photo import FamilyPhoto
from app.services.image_processing import generate_cards_from_bytes

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

def generate_and_store_cards(
    db: Session,
    user_id: str,
    img_bytes: bytes,
) -> list[str]:
    """YOLO → 카드 PIL → S3 저장 → DB 저장 → URL 리스트 반환"""
    card_urls: list[str] = []
    for idx, card in enumerate(generate_cards_from_bytes(img_bytes)):
        url = upload_pil_image_to_s3(
            card,
            user_id,
            filename=f"card_{idx}.jpg",
        )
        # 카드 파일 DB 기록
        photo = FamilyPhoto(user_id=user_id, file_path=url)
        db.add(photo)
        card_urls.append(url)
    return card_urls