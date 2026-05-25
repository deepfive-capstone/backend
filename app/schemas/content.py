#프론트<->백엔드

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, HttpUrl, ConfigDict

#프론트->백엔드 요청 형식
class ContentCreateRequest(BaseModel):
    url:HttpUrl

#백엔드->프론트 response 형식(DB 저장 시 변경)
class ContentCardResponse(BaseModel):
    content_id:int
    url:str
    video_id:Optional[str]=None
    platform: str="YouTube"
    title: str
    channel:Optional[str]=None
    thumbnail:Optional[str]=None
    category:str
    summary:str
    status: str
    created_at:Optional[datetime]=None
    updated_at:Optional[datetime]=None

    model_config=ConfigDict(from_attributes=True) #SQLAlchemy DB객체를 그대로 응답할 때 필요

class ContentStatusRequest(BaseModel):
    status:str

class ContentListResponse(BaseModel):
    total:int
    items: List[ContentCardResponse]

class ContentDeleteRequest(BaseModel):
    content_ids:List[int]

class ContentDeleteResponse(BaseModel):
    delete_count:int
    deleted_ids:List[int]
    message:str