#백엔드<->DB
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.modules.card_generator import build_content_card
from app.services.ai_service import analyze_youtube_url
from app.models.content import Content
from app.models.category import Category

#AI 호출 중심
async def get_content_card(url:str)->dict:
    ai_result=await analyze_youtube_url(url)
    content_card=build_content_card(url=url, ai_result=ai_result)
    
    return content_card

#DB에서 가져온 정보, 프론트 응답 형태로 변경
def content_to_card(content:Content, category_name:Optional[str])->dict:
    return{
        "content_id": content.content_id,
        "url": content.original_url,
        "video_id":content.video_id,
        "title": content.title,
        "channel": content.channel_name,
        "platform":content.platform_type,
        "thumbnail": content.thumbnail_url,
        "category": category_name,
        "summary": content.ai_summary,
        "status": content.status,
        "created_at":content.created_at,
        "updated_at":content.updated_at
    }

#저장된 카드 목록 DB에서 꺼내오기
def get_content_list(
        db:Session,
        categories: Optional[List[str]]=None
)->dict:
    #content_id에 연결된 content_name 가져오긴
    query=(
        db.query(Content, Category.name)
        .join(Category,Content.category_id==Category.category_id)
    )
    if categories:
        query=query.filter(Category.name.in_(categories))

    results=(
        query
        .order_by(Content.created_at.desc())
        .all()
    )
    items = []

    for content, category_name in results:
        item = content_to_card(content, category_name)
        items.append(item)

    return{
        "total": len(items),
        "items": items
    }

def get_content_detail(db:Session, content_id:int)->dict:
    result=(
        db.query(Content,Category.name)
        .join(Category,Content.category_id==Category.category_id)
        .filter(Content.content_id==content_id)
        .one_or_none()
    )
    if not result:
        raise HTTPException(
            status_code=404,
            detail="해당 콘텐츠를 찾을 수 없습니다."
        )
    content, category_name = result

    return content_to_card(content,category_name)

def content_status(db:Session, content_id:int, status:str)->dict:
    result=(
        db.query(Content,Category.name)
        .join(Category, Content.category_id==Category.category_id)
        .filter(Content.content_id==content_id)
        .one_or_none()
    )
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="해당 콘텐츠를 찾을 수 없습니다."
        )

    content, category_name=result
    content.status= status

    db.commit() #DB에 저장
    db.refresh(content) #최신값 불러오기

    return content_to_card(content, category_name)

def delete_contents(db:Session, content_ids:List[int])->dict:
    contents=(
        db.query(Content)
        .filter(Content.content_id.in_(content_ids))
        .all()
    )
    if not contents:
        raise HTTPException(
            status_code=404,
            detail="해당 콘텐츠를 찾을 수 없습니다."
        )
    deleted_ids=[content.content_id for content in contents]

    for content in contents:
        db.delete(content)

    db.commit()
    
    return{
        "deleted_count":len(deleted_ids),
        "deleted_ids":deleted_ids,
        "message": "선택한 콘텐츠가 삭제되었습니다."
    }