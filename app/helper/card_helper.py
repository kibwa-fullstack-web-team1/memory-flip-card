from sqlalchemy.orm import Session
from app.models.upload_photo import FamilyPhoto
from app.models.card_image import CardImage
from app.core.s3_service import upload_pil_image_to_s3
from typing import List

def create_and_store_cards(
    db: Session,
    family_photo_id: int,
    user_id: str,
    img_bytes: bytes,
    difficulty: str = "easy"
) -> List[CardImage]:
    """카드 이미지 생성 및 저장"""
    cards = generate_cards_from_bytes(img_bytes, difficulty=difficulty)
    card_records = []
    
    for idx, card_img in enumerate(cards):
        # S3에 카드 이미지 업로드
        card_url = upload_pil_image_to_s3(
            card_img, 
            user_id, 
            folder="card_images",
            filename=f"card_{idx+1}.jpg"
        )
        
        # DB에 카드 정보 저장
        card_record = CardImage(
            family_photo_id=family_photo_id,
            card_url=card_url,
            card_index=idx
        )
        db.add(card_record)
        card_records.append(card_record)
    
    return card_records

def get_cards_by_photo_id(db: Session, family_photo_id: int) -> List[CardImage]:
    """특정 원본 사진의 카드 이미지들 조회"""
    return db.query(CardImage).filter(
        CardImage.family_photo_id == family_photo_id
    ).order_by(CardImage.card_index).all()