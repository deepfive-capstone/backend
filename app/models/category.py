from sqlalchemy import Column, BigInteger, String
from app.db.database import Base

class Category(Base):
    __tablename__ = 'categories'

    category_id=Column(BigInteger, primary_key=True, autoincrement=True)
    name=Column(String(50), nullable=False)
