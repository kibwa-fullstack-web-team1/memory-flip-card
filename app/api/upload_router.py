from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from typing import List

from app.deps.db import get_db
from app.helper.photo_helper import save_photo_record
from app.models.upload_photo import FamilyPhoto
from app.models.card_image import CardImage
from app.helper.photo_helper import check_photo_duplicate
from app.services.image_processing import generate_cards_from_bytes
from app.core.s3_service import upload_file_to_s3, download_file_from_s3, upload_pil_image_to_s3
from app.utils.functions import calculate_file_hash

router = APIRouter()

# 원본 사진 업로드 api
@router.post("/family-photos")
async def upload_family_photo(
    user_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        # 파일 내용 읽기
        file_contents = await file.read()
        await file.seek(0)

        # 파일 해시 계산
        file_hash = calculate_file_hash(file_contents)

        # 중복 확인
        existing_photo = check_photo_duplicate(db, user_id, file_hash)
        if existing_photo:
            return JSONResponse(status_code=200, content={
                "message": "이미 업로드된 파일입니다. 건너뜁니다.",
                "photo_id": existing_photo.id,
                "file_url": existing_photo.file_path
            })

        # S3 업로드 서비스 호출
        s3_url = upload_file_to_s3(file, user_id)

        # DB 저장
        photo_record = save_photo_record(db, user_id, s3_url, file_hash)
    
        return JSONResponse(status_code=200, content={
            "message": "업로드 성공",
            "photo_id": photo_record.id,
            "file_url": s3_url
        })
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"업로드 실패: {str(e)}")

# YOLO 기반 사진 업로드 및 카드 생성 통합 API
@router.post("/family-photos/cards-yolo")
async def generate_cards_from_existing_photos(
    user_id: str = Form(...),
    db: Session = Depends(get_db)
):
    # 1. user_id로 DB에서 해당 사용자의 모든 사진 조회
    photo_records = db.query(FamilyPhoto).filter(FamilyPhoto.user_id == user_id).all()
    if not photo_records:
        raise HTTPException(status_code=404, detail="해당 유저의 사진이 없습니다.")

    all_card_urls = []
    new_cards = []

    for photo_record in photo_records:
        # 이미 해당 사진으로 생성된 카드가 있는지 확인
        existing_cards = db.query(CardImage).filter(CardImage.family_photo_id == photo_record.id).all()
        if existing_cards:
            print(f"Photo ID {photo_record.id}에 대한 카드가 이미 존재하여 건너뜁니다.")
            all_card_urls.extend([card.card_url for card in existing_cards])
            continue
        
        try:
            # 2. S3에서 사진 다운로드
            img_bytes_io = download_file_from_s3(photo_record.file_path)
            img_bytes = img_bytes_io.read()

            # 3. YOLO로 얼굴 감지 후 카드 이미지(PIL) 리스트 생성
            card_pil_images = generate_cards_from_bytes(img_bytes)

            if not card_pil_images:
                print(f"Photo ID {photo_record.id}에서 얼굴을 찾지 못했습니다.")
                continue

            # 4. 생성된 카드 이미지들을 S3에 업로드하고 DB 저장 준비
            for idx, card_pil_img in enumerate(card_pil_images):
                card_url = upload_pil_image_to_s3(
                    img=card_pil_img,
                    user_id=user_id,
                    folder="card_images",
                    filename=f"photo_{photo_record.id}_card_{idx}.jpg"
                )
                
                new_card = CardImage(
                    family_photo_id=photo_record.id,
                    card_url=card_url,
                    card_index=idx
                )
                new_cards.append(new_card)
                all_card_urls.append(card_url)

        except Exception as e:
            print(f"[ERROR] Photo ID {photo_record.id} 처리 중 오류 발생: {e}")
            db.rollback()
            continue

    if not new_cards:
        if all_card_urls:
            return JSONResponse(status_code=200, content={
                "message": "새로 생성된 카드는 없지만, 기존 카드를 반환합니다.",
                "card_urls": all_card_urls
            })
        raise HTTPException(status_code=400, detail="카드 생성에 적합한 사진이 없거나 처리 중 오류가 발생했습니다.")

    try:
        db.add_all(new_cards)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"DB 저장 중 오류 발생: {e}")

    return JSONResponse(status_code=200, content={
        "message": f"총 {len(all_card_urls)}장의 카드가 준비되었습니다.",
        "card_urls": all_card_urls
    })

# dlib 기반, 사용자별 모든 사진에서 카드 생성 API
# @router.post("/family-photos/cards-dlib")
# async def generate_cards_with_dlib(
#     user_id: str = Form(...),
#     db: Session = Depends(get_db)
# ):
#     # 1. user_id로 DB에서 원본 사진 정보들 가져오기
#     photo_records = db.query(FamilyPhoto).filter(FamilyPhoto.user_id == user_id).all()
#     if not photo_records:
#         raise HTTPException(status_code=404, detail="해당 사용자의 사진을 찾을 수 없습니다.")

#     card_urls = []
#     new_cards = []

#     try:
#         for photo_record in photo_records:
#             # 이미 처리된 사진인지 확인
#             existing_card = db.query(CardImage).filter(CardImage.family_photo_id == photo_record.id).first()
#             if existing_card:
#                 print(f"Photo ID {photo_record.id}는 이미 처리되었으므로 건너뜁니다.")
#                 continue

#             try:
#                 # 2. S3에서 이미지 파일 다운로드
#                 img_bytes_io = download_file_from_s3(photo_record.file_path)
#                 img_bytes = img_bytes_io.read()

#                 # 3. dlib으로 얼굴 크롭하여 카드 이미지 생성
#                 card_pil_img = crop_face_from_bytes(img_bytes)

#                 # 4. 생성된 카드 이미지를 S3에 업로드
#                 card_url = upload_pil_image_to_s3(
#                     img=card_pil_img,
#                     user_id=photo_record.user_id,
#                     folder="card_images"
#                 )

#                 # 5. 새 카드 정보를 DB에 저장할 준비
#                 new_card = CardImage(
#                     family_photo_id=photo_record.id,
#                     card_url=card_url,
#                     card_index=0  # dlib은 사진 당 카드 1개만 생성
#                 )
#                 new_cards.append(new_card)
#                 card_urls.append(card_url)
            
#             except ValueError as ve:
#                 # 특정 사진에서 얼굴을 찾지 못하면 건너뛰기
#                 print(f"Photo ID {photo_record.id}에서 얼굴을 찾지 못했습니다: {ve}")
#                 continue

#         if not new_cards:
#             raise HTTPException(status_code=400, detail="카드 생성에 적합한 얼굴을 가진 사진이 없습니다.")

#         db.add_all(new_cards)
#         db.commit()

#         return JSONResponse(status_code=200, content={
#             "message": "dlib 기반 카드 생성 완료",
#             "card_urls": card_urls
#         })
#     except Exception as e:
#         db.rollback()
        # raise HTTPException(status_code=500, detail=f"카드 생성 중 오류 발생: {str(e)}")