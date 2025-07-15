import os
import boto3
from functools import lru_cache

class Config:
    """기본 설정"""
    PHASE = 'default'
    
    # 데이터베이스 설정
    DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://user:password@localhost/dbname')
    
    # AWS S3 설정
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
    AWS_S3_BUCKET_NAME = os.environ.get('AWS_S3_BUCKET_NAME', '')
    AWS_S3_REGION = os.environ.get('AWS_S3_REGION', 'ap-northeast-2')

class DevelopmentConfig(Config):
    """개발 환경 설정"""
    PHASE = 'development'

class ProductionConfig(Config):
    """프로덕션 환경 설정"""
    PHASE = 'production'

config_by_name = dict(
    development=DevelopmentConfig,
    production=ProductionConfig,
)

# 현재 환경에 따른 설정 선택
def get_config():
    """환경에 따른 설정을 반환합니다."""
    env = os.environ.get('FLASK_ENV', 'development')
    return config_by_name.get(env, DevelopmentConfig)

# 현재 설정 인스턴스
current_config = get_config()()

# 함수 결과를 메모리에 저장하고 재사용
@lru_cache()
def get_settings():
    """캐시된 설정을 반환합니다."""
    return current_config

@lru_cache()
def get_s3_client():
    """S3 클라이언트를 반환합니다."""
    return boto3.client(
        "s3",
        region_name=current_config.AWS_S3_REGION,
        aws_access_key_id=current_config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=current_config.AWS_SECRET_ACCESS_KEY
    )
