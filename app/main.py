from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.routers import content
from app.db.session import get_db

app = FastAPI()

app.include_router(content.router)

@app.get("/")
def read_root():
    return {"message": "Backend is running!"}

@app.get("/test-db", tags=["DB Test"])
def test_db_connection(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"message": "DB 연결이 성공적으로 완료되었습니다! 🚀"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB 연결 실패: {str(e)}")
