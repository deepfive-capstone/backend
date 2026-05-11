from fastapi import APIRouter
from app.services.content_service import get_content_card
from app.schemas.content import ContentCreateRequest, ContentResponse

router=APIRouter(prefix="/contents", tags=["contents"])

@router.post("",response_model=ContentResponse)
async def create_content(request:ContentCreateRequest):
    return await get_content_card(str(request.url))