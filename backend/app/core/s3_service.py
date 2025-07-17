import io
import uuid
from PIL import Image
from datetime import datetime
from fastapi import UploadFile
from app.config.config import get_s3_client,get_settings

# S3 업로드 함수, 원본 사진 업로드
def upload_file_to_s3(file: UploadFile, user_id: str, folder: str = "family_photos") -> str:
    """
    S3에 파일을 업로드하고 URL을 반환합니다.
    
    Args:
        file: 업로드할 파일
        user_id: 사용자 ID
        folder: S3 폴더명
        
    Returns:
        str: 업로드된 파일의 S3 URL
    """
    s3_client = get_s3_client()
    config = get_settings()
    
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    unique_filename = f"{user_id}_{timestamp}_{uuid.uuid4().hex}_{file.filename}"
    s3_key = f"{folder}/{unique_filename}"

    # S3에 파일 업로드
    s3_client.upload_fileobj(
        file.file,
        config.AWS_S3_BUCKET_NAME,
        s3_key
    )

    file_url = f"https://{current_config.AWS_S3_BUCKET_NAME}.s3.{current_config.AWS_S3_REGION}.amazonaws.com/{s3_key}"
    return file_url

def delete_file_from_s3(s3_key: str) -> bool:
    """
    S3에서 파일을 삭제합니다.
    
    Args:
        s3_key: 삭제할 파일의 S3 키
        
    Returns:
        bool: 삭제 성공 여부
    """
    try:
        s3_client = get_s3_client()
        config = get_settings()

        s3_client.delete_object(
            Bucket=config.AWS_S3_BUCKET_NAME,
            Key=s3_key
        )
        return True
    except Exception:
        return False

#YOLO로 객체를 탐지한 이미지 업로드
def upload_pil_image_to_s3(
    img: Image.Image,
    user_id: str,
    folder: str = "card_images",
    filename: str | None = None
) -> str:
    """
    PIL 이미지를 JPEG 바이트로 변환해 S3에 저장하고 URL 반환
    - img      : PIL.Image 객체 (이미 YOLO 크롭·정형화 완료된 카드)
    - user_id  : 경로 구분용
    - folder   : S3 버킷 내부 폴더 (기본 card_images/)
    - filename : 직접 지정하고 싶을 때(확장자는 .jpg 권장)
    """
    s3_client = get_s3_client()
    config = get_settings()
    filename  = filename or f"{uuid.uuid4().hex}.jpg"
    s3_key    = f"{folder}/{user_id}/{filename}"

    # PIL → 메모리버퍼(JPEG) 변환
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    buf.seek(0)

    # 업로드
    s3_client.upload_fileobj(
        buf,
        config.AWS_S3_BUCKET_NAME,
        s3_key
    )

    return (
        f"https://{config.AWS_S3_BUCKET_NAME}"
        f".s3.{config.AWS_S3_REGION}.amazonaws.com/{s3_key}"
    )