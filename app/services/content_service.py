# 백엔드 <-> DB
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.modules.card_generator import build_content_card
from app.services.ai_service import analyze_youtube_url
from app.services.category_service import get_category_id_by_name
from app.models.content import Content
from app.models.category import Category



async def get_content_card(url: str, db: Session, user_id:int) -> dict:
    # 1. AI 서버 분석 요청
    ai_result = await analyze_youtube_url(url)

    # 2. 카드 데이터 구성
    content_card = build_content_card(url=url, ai_result=ai_result)

    # 3. categories 테이블에서 category_id 조회 (없으면 자동 생성)
    category_name = content_card.get("category", "기타")
    category_id = get_category_id_by_name(db, category_name)

    # 4. 실제 DB 스키마 컬럼 명칭에 맞춰 Content 객체 생성
    new_content = Content(
        user_id=user_id,
        category_id=category_id,
        original_url=url,
        video_id=content_card.get("video_id"),  # DB 반영
        title=content_card.get("title") or "",
        channel_name=content_card.get("channel") or "",  # DB 반영 (channel -> channel_name)
        thumbnail_url=content_card.get("thumbnail_url") or "",
        ai_summary=content_card.get("summary"),
        platform_type="YouTube",  # DB 반영 (platform -> platform_type)
        status="unread",
    )

    try:
        db.add(new_content)
        db.commit()
        db.refresh(new_content)  # DB에서 content_id, created_at 등 기본 키와 서버 기본값 생성 반영
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"DB 저장 실패: {str(e)}")

    # 5. DB 저장 결과를 ContentResponse 스키마 규격에 맞춰 응답 dict 구성
    return {
        "content_id": new_content.content_id,
        "url": url,
        "video_id": new_content.video_id,
        "platform": new_content.platform_type,
        "title": new_content.title,
        "channel": new_content.channel_name,
        "thumbnail": new_content.thumbnail_url,
        "category": category_name,
        "category_id": new_content.category_id,
        "summary": new_content.ai_summary,
        "status": new_content.status,
        "created_at": new_content.created_at,
    }

async def get_contents_list(db: Session, categories: list[str] = None) -> list:
    query = db.query(Content, Category.name).outerjoin(Category, Content.category_id == Category.category_id)
    if categories:
        query = query.filter(Category.name.in_(categories))
    
    results = query.all()
    
    items = []
    for content, category_name in results:
        items.append({
            "content_id": content.content_id,
            "video_id": content.video_id,
            "channel": content.channel_name,
            "title": content.title,
            "summary": content.ai_summary,
            "thumbnail": content.thumbnail_url,
            "category": category_name or "기타",
            "status": content.status,
        })
    return items

async def update_status(content_id: int, status: str, db: Session) -> dict:
    content = db.query(Content).filter(Content.content_id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="콘텐츠를 찾을 수 없습니다.")
    
    content.status = status
    try:
        db.commit()
        db.refresh(content)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"상태 업데이트 실패: {str(e)}")
        
    return {"message": "상태가 성공적으로 업데이트되었습니다."}

async def delete_contents(content_ids: list[int], db: Session) -> dict:
    try:
        db.query(Content).filter(Content.content_id.in_(content_ids)).delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"콘텐츠 삭제 실패: {str(e)}")
    return {"message": "콘텐츠가 성공적으로 삭제되었습니다."}