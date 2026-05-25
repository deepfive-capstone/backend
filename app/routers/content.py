from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.services.content_service import get_content_card, get_content_list, get_content_detail, content_status, delete_contents
from app.schemas.content import ContentCreateRequest, ContentCardResponse, ContentListResponse, ContentStatusRequest, ContentDeleteResponse, ContentDeleteRequest
from app.db.session import get_db

router=APIRouter(prefix="/contents", tags=["contents"])

@router.post("",response_model=ContentCardResponse)
async def create_content(request:ContentCreateRequest):
    return await get_content_card(str(request.url))

@router.get("",response_model=ContentListResponse)
def read_content_lists(
    category:Optional[List[str]]=Query(default=None),
    db:Session=Depends(get_db)
):
    return get_content_list(db=db, categories=category)

@router.get("/{content_id}", response_model=ContentCardResponse)
def read_content_detail(
    content_id:int,
    db: Session=Depends(get_db)
):
    return get_content_detail(db=db, content_id=content_id)

@router.patch("/{content_id}/status", response_model=ContentCardResponse)
def update_content_status(
    content_id:int,
    request: ContentStatusRequest,
    db:Session=Depends(get_db)
):
    return content_status(
        db=db,
        content_id=content_id,
        status=request.status
    )

@router.delete("/{content_id}", response_model=ContentDeleteResponse)
def remove_content(
    request:ContentDeleteRequest,
    db:Session=Depends(get_db)
):
    return delete_contents(db=db, content_ids=request.content_ids)