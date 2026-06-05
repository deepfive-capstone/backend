from sqlalchemy.orm import Session
from app.models.category import Category


def get_category_id_by_name(db: Session, name: str) -> int:
    """
    카테고리 이름으로 category_id를 조회한다.
    없으면 새로 생성 후 반환한다 (Upsert 방식).
    """
    category = db.query(Category).filter(Category.name == name).first()
    if category is None:
        # categories 테이블에 없으면 새로 삽입
        category = Category(name=name)
        db.add(category)
        db.commit()
        db.refresh(category)
    return category.category_id
