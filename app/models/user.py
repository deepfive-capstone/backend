from sqlalchemy import Column, BigInteger, String, DateTime, func
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=True)
    nickname = Column(String(50), nullable=False)
    provider = Column(String(20), nullable=False, default="google")
    google_sub = Column(String(255), unique=True, nullable=True)
    created_at = Column(DateTime, server_default=func.now())