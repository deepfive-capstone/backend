# 백엔드 -> DB 저장
# DB -> 백엔드 응답

from sqlalchemy import Column, BigInteger, String, Text, DateTime, ForeignKey, Integer
from sqlalchemy.sql import func
from app.db.database import Base


class Content(Base):
    __tablename__ = "contents"

    content_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=True)  # DB 컬럼 반영
    category_id = Column(
        Integer, ForeignKey("categories.category_id"), nullable=True
    )  # DB 컬럼 타입 반영(INTEGER, Nullable)
    original_url = Column(Text, nullable=False)
    video_id = Column(String(100), nullable=True)  # DB 컬럼 반영
    title = Column(String(255), nullable=False)
    channel_name = Column(
        String(255), nullable=True
    )  # DB 컬럼 반영 (channel -> channel_name)
    thumbnail_url = Column(Text, nullable=True)
    ai_summary = Column(
        Text, nullable=True
    )  # DB TEXT 용량 확장 매핑 반영
    platform_type = Column(
        String(50), nullable=True, default="YouTube"
    )  # DB 컬럼 반영
    status = Column(String(50), nullable=True, default="unread")  # DB ENUM 기본값 매핑
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )