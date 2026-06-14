from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.models.user import User
from app.modules.user import get_current_user
from app.services.content_service import get_content_card, get_contents_list, update_status, delete_contents
from app.schemas.content import ContentCreateRequest, ContentResponse, ContentStatusRequest, ContentDeleteRequest
from app.db.session import get_db

router = APIRouter(prefix="/contents", tags=["contents"])


@router.post("", response_model=ContentResponse)
async def create_content(
    request: ContentCreateRequest, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    ):
    return await get_content_card(
        url=str(request.url), 
        db=db,
        user_id=current_user.user_id,
    )

@router.get("")
async def list_contents(category: list[str] = Query(None), db: Session = Depends(get_db)):
    return await get_contents_list(db, category)

@router.patch("/{content_id}/status")
async def update_content_status(content_id: int, request: ContentStatusRequest, db: Session = Depends(get_db)):
    return await update_status(content_id, request.status, db)

@router.delete("/{content_id}")
async def delete_content(content_id: int, request: ContentDeleteRequest, db: Session = Depends(get_db)):
    return await delete_contents(request.content_ids, db)