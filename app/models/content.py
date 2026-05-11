#백엔드 -> DB 저장
#DB -> 백엔드 응답

from sqlalchemy import Column, BigInteger, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.database import Base

class Content(Base):
    __tablename__ = 'contents'

    #nullable=False 값이 필수로 들어가야됨.
    content_id=Column(BigInteger, primary_key=True, autoincrement=True)
    category_id=Column(BigInteger,ForeignKey("categories.category_id"),nullable=False)
    original_url=Column(Text,nullable=False)
    #video_id=Column(String(30),nullable=False)
    title=Column(String(255), nullable=False)
    channel=Column(String(50),nullable=False)
    thumbnail_url=Column(Text,nullable=False)
    ai_summary=Column(String(500),nullavle=False)
    status=Column(String(10),nullable=False, default='saved')
    created_at=Column(DateTime,server_default=func.now(),nullable=False) #값을 따로 안 넣으면, 기본값으로 현재 시간
    #updated_at=Column(DateTime,server_default=func.now(),onupdate=func.now(),nullable=False)