from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.config import current_config

# 데이터베이스 URL 설정
SQLALCHEMY_DATABASE_URL = current_config.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def create_tables():
    """데이터베이스 테이블을 생성합니다."""
    Base.metadata.create_all(bind=engine)
