import os
import boto3
from functools import lru_cache
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """애플리케이션 설정"""
    # 데이터베이스 설정
    database_url: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")
    
    # AWS S3 설정
    aws_access_key_id: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    aws_secret_access_key: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    aws_s3_bucket_name: str = os.getenv("AWS_S3_BUCKET_NAME", "")
    aws_s3_region: str = os.getenv("AWS_S3_REGION", "ap-northeast-2")
    
    class Config:
        env_file = ".env"

#함수 결과를 메모리에 저장하고 재사용
@lru_cache()
def get_settings():
    """캐시된 설정을 반환합니다."""
    return Settings()

@lru_cache()
def get_s3_client():
    """S3 클라이언트를 반환합니다."""
    settings = get_settings()
    return boto3.client(
        "s3",
        region_name=settings.aws_s3_region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key
    )