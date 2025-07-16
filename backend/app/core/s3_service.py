import uuid
from datetime import datetime
from fastapi import UploadFile
from app.config.config import get_s3_client, current_config

# S3 업로드 함수
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
    
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    unique_filename = f"{user_id}_{timestamp}_{uuid.uuid4().hex}_{file.filename}"
    s3_key = f"{folder}/{unique_filename}"

    # S3에 파일 업로드
    s3_client.upload_fileobj(
        file.file,
        current_config.AWS_S3_BUCKET_NAME,
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
        s3_client.delete_object(
            Bucket=current_config.AWS_S3_BUCKET_NAME,
            Key=s3_key
        )
        return True
    except Exception:
        return False