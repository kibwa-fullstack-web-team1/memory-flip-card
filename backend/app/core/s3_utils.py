import os
import boto3
import uuid
from datetime import datetime
from fastapi import UploadFile
from dotenv import load_dotenv

load_dotenv()

# S3 설정
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")
AWS_S3_REGION = os.getenv("AWS_S3_REGION")

s3_client = boto3.client(
    "s3",
    region_name=AWS_S3_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# S3 업로드 함수
def upload_to_s3(file: UploadFile, user_id: str) -> str:
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    unique_filename = f"{user_id}_{timestamp}_{uuid.uuid4().hex}_{file.filename}"
    s3_key = f"family_photos/{unique_filename}"

    # S3에 파일 업로드
    s3_client.upload_fileobj(
        file.file,
        AWS_S3_BUCKET_NAME,
        s3_key,
        # ExtraArgs={"ACL": "public-read", "ContentType": file.content_type}
    )

    file_url = f"https://{AWS_S3_BUCKET_NAME}.s3.{AWS_S3_REGION}.amazonaws.com/{s3_key}"
    return file_url