from app.core.database import SessionLocal

def get_db():
    """
    요청마다 새로운 DB 세션을 생성하고, 요청 처리가 완료되면 세션을 닫습니다.
    FastAPI의 의존성 주입 시스템에서 사용됩니다.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()