from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.upload_router import router as upload_router
from app.api.list_router import router as list_router
from app.api.game_router import router as game_router
from app.core.database import create_tables

# Import all models to ensure they are registered with SQLAlchemy Base.metadata
import app.models

def create_app() -> FastAPI:
    # 데이터베이스 테이블 생성
    create_tables()
    
    app = FastAPI(title="Memory Flip Card API")

    # CORS 설정
    origins = [
        "http://localhost:5173", # react 개발 서버 포트
        "http://localhost", # 개발 환경
        "http://13.251.163.144:5173", # 프론트엔드 배포 서버 주소 
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"], # 모든 HTTP 메소드 허용
        allow_headers=["*"], # 모든 헤더 허용
    )
    
    # 라우터 등록
    app.include_router(upload_router, prefix="/upload", tags=["Upload"])
    app.include_router(list_router, prefix="/list", tags=["List"])
    app.include_router(game_router, prefix="/games", tags=["Record"])
    
    @app.get("/", tags=["Root"])
    def read_root():
        return {"message": "Welcome to Memory Flip Card API"}
    
    return app
