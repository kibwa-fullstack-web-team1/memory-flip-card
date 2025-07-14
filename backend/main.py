import uvicorn
# app 패키지에서 create_app 함수 임포트
from app import create_app

# FastAPI 앱 생성
app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
