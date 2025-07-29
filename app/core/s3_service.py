import io
import uuid
from PIL import Image
from datetime import datetime
from fastapi import UploadFile
from app.config.config import get_s3_client, get_settings

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

    file_url = f"https://{config.AWS_S3_BUCKET_NAME}.s3.{config.AWS_S3_REGION}.amazonaws.com/{s3_key}"
    return file_url

def download_file_from_s3(s3_url: str) -> io.BytesIO:
    """
    S3 URL에서 파일을 다운로드하여 메모리 내 바이트 스트림으로 반환합니다.
    URL에서 버킷 이름과 키를 직접 파싱합니다.

    Args:
        s3_url: 다운로드할 파일의 전체 S3 URL

    Returns:
        io.BytesIO: 파일 데이터가 담긴 메모리 버퍼
    """
    try:
        s3_client = get_s3_client()
        
        # URL에서 버킷 이름과 키 분리
        if not s3_url.startswith('https://'):
            raise ValueError(f"잘못된 S3 URL 형식입니다: {s3_url}")

        parts = s3_url.replace('https://', '').split('/')
        domain = parts[0]
        key = '/'.join(parts[1:])
        
        bucket_name = domain.split('.s3.')[0]

        if not bucket_name or not key:
            raise ValueError(f"URL에서 버킷 이름과 키를 파싱할 수 없습니다: {s3_url}")

        buffer = io.BytesIO()
        s3_client.download_fileobj(
            Bucket=bucket_name,
            Key=key,
            Fileobj=buffer
        )
        buffer.seek(0)
        return buffer
    except Exception as e:
        print(f"S3에서 파일을 다운로드하는 중 오류 발생: {e}")
        raise

def delete_file_from_s3(s3_url: str) -> bool:
    """
    S3에서 파일을 삭제합니다.
    
    Args:
        s3_url: 삭제할 파일의 S3 URL
        
    Returns:
        bool: 삭제 성공 여부
    """
    try:
        s3_client = get_s3_client()
        
        if not s3_url.startswith('https://'):
             raise ValueError(f"잘못된 S3 URL 형식입니다: {s3_url}")

        parts = s3_url.replace('https://', '').split('/')
        domain = parts[0]
        key = '/'.join(parts[1:])
        bucket_name = domain.split('.s3.')[0]

        if not bucket_name or not key:
            raise ValueError(f"URL에서 버킷 이름과 키를 파싱할 수 없습니다: {s3_url}")

        s3_client.delete_object(
            Bucket=bucket_name,
            Key=key
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