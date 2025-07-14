from fastapi import UploadFile
import uuid
from datetime import datetime
from app.core.config import get_s3_client, get_settings

def upload_photo_to_s3(file: UploadFile, user_id: str) -> str:
    """
    S3에 사진을 업로드하고 URL을 반환합니다.
    
    Args:
        file: 업로드할 파일
        user_id: 사용자 ID
        
    Returns:
        str: 업로드된 파일의 S3 URL
    """
    settings = get_settings()
    s3_client = get_s3_client()
    
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    unique_filename = f"{user_id}_{timestamp}_{uuid.uuid4().hex}_{file.filename}"
    s3_key = f"family_photos/{unique_filename}"

    # S3에 파일 업로드
    s3_client.upload_fileobj(
        file.file,
        settings.aws_s3_bucket_name,
        s3_key
    )

    file_url = f"https://{settings.aws_s3_bucket_name}.s3.{settings.aws_s3_region}.amazonaws.com/{s3_key}"
    return file_url