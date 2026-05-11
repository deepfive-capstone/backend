#백엔드<->DB
from app.modules.card_generator import build_content_card
from app.services.ai_service import analyze_youtube_url

async def get_content_card(url:str)->dict:
    ai_result=await analyze_youtube_url(url)
    content_card=build_content_card(url=url, ai_result=ai_result)
    
    return content_card()