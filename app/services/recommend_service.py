from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.recommend import RecommendRequest,RecommendResponse
from app.services.ai_service import recommend_videos
from app.models.content import Content
from app.models.category import Category

async def get_recommend_videos(
    request: RecommendRequest,
    db: Session
) -> dict:
    #DB 조회
    result = (
        db.query(Content)
        .join(Category, Content.category_id == Category.category_id)
        .filter(Content.content_id == request.content_id)
        .first()
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="해당 콘텐츠를 찾을 수 없습니다."
        )
    
    content, category_name = result

    #추천영상 API 호출
    ai_result = await recommend_videos(
        title=content.title,
        category=category_name,
        limit=request.limit
    )

    return RecommendResponse(
    recommendations=ai_result["recommendations"]
)