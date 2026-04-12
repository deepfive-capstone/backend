from fastapi import APIRouter
from app.services.content_service import get_preview_card

router=APIRouter(prefix="/content", tags=["content"])

@router.get("/preview")
def preview_content():
    return get_preview_card()