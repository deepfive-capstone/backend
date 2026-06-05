from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.schemas.recommend import RecommendRequest, RecommendResponse
from app.services.recommend_service import get_recommend_videos

from app.db.session import get_db

router = APIRouter(
    prefix="/recommend",
    tags=["Recommendation"]
)


@router.post("", response_model=RecommendResponse)
async def recommend_videos(
    request: RecommendRequest,
    db:Session=Depends(get_db)
):
    return await get_recommend_videos(request=request, db=db)