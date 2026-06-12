from pydantic import BaseModel
from typing import List, Optional

#프론트->백엔드 
class RecommendRequest(BaseModel):
    content_id:int
    limit: int = 5

class RecommendedVideo(BaseModel):
    video_id: str
    title: str
    channel: str
    thumbnail_url: Optional[str] = None
    youtube_url: str

#백엔드->프론트 
class RecommendResponse(BaseModel):
    recommendations: List[RecommendedVideo]