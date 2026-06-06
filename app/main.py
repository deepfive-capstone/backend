from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.routers import content, recommend, user
from app.db.session import get_db

app = FastAPI()

# CORS 미들웨어 추가 (Flutter Web 브라우저 요청 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(content.router)
app.include_router(recommend.router)
app.include_router(user.router)

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
