#프론트<->백엔드

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl, ConfigDict

#프론트->백엔드 요청 형식
class ContentCreateRequest(BaseModel):
    url:HttpUrl

#백엔드->프론트 response 형식(DB 저장 시 변경)
class ContentResponse(BaseModel):
    url:str
    video_id:Optional[str]=None
    platform: str="YouTube"
    title: Optional[str]=None
    channel:Optional[str]=None
    thumbnail:Optional[str]=None
    category:str
    category_id:Optional[int]=None
    summary:str
    status: str='unread'
    created_at:Optional[datetime]=None

    model_config=ConfigDict(from_attributes=True) #SQLAlchemy DB객체를 그대로 응답할 때 필요

class ContentStatusRequest(BaseModel):
    status:str

class ContentDeleteRequest(BaseModel):
    content_ids: list[int]