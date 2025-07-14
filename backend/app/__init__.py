from fastapi import FastAPI
from app.api.upload_router import router as upload_router
from app.api.list_router import router as list_router
from app.core.database import create_tables

def create_app() -> FastAPI:
    # 데이터베이스 테이블 생성
    create_tables()
    
    app = FastAPI(title="Memory Flip Card API")
    
    # 라우터 등록
    app.include_router(upload_router, prefix="/upload", tags=["Upload"])
    app.include_router(list_router, prefix="/list", tags=["List"])
    
    @app.get("/", tags=["Root"])
    def read_root():
        return {"message": "Welcome to Memory Flip Card API"}
    
    return app
