#AI->백엔드 응답

def build_content_card(url:str, ai_result:dict)->dict:
    video_id=ai_result.get("video_id")
    category=ai_result.get("category")
    summary=ai_result.get("summary")
    #channel=ai_result.get("channel")
    #title=ai_result.get("title")
    #thumbnail=ai_result.get("thumbnail_url")
    return{
        "url":url,
        "video_id":video_id,
        "category":category,
        "summary":summary,
        "platform":"YouTube",
        #"channel":channel,
        #"title":"title,
        #"thumbnail_url":thumnail,
    }