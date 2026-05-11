import httpx
from fastapi import HTTPException

AI_SERVER_URL="http://127.0.0.1:8001"

#URL 문자열을 받아서 AI서버에 넘기고, AI응답 JSON을 dict 형태로 돌려주는 함수
async def analyze_youtube_url(url:str)-> dict: 
    try:
        #AI서버 호출하는 부분
        async with httpx.AsyncClient(timeout=120.0) as client:
            response=await client.post( 
                f"{AI_SERVER_URL}/analyze",
                json={"url":url}
            )
               
            
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="AI 서버에 연결할 수 없습니다."
        )
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="AI 서버 응답 시간이 초과되었습니다."
        )
    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="AI 서버 요청 중 오류가 발생하였습니다."
        )
    if response.status_code !=200:
        raise HTTPException(
            status_code=502,
            detail=f"AI 분석 요청 실패. 응답코드: {response.status_code}"
        )
    
    try:
        #AI서버 응답을 dict로 바꾸기
        data=response.json()
    except ValueError:
        raise HTTPException(
            status_code=502,
            detail="AI 응답이 JSON 형식이 아닙니다."
        )
    
    required_fields=["video_id", "category","summary"]
    missing_fields=[field for field in required_fields if field not in data]

    if missing_fields:
        raise HTTPException(
            status_code=502,
            detail=f"AI 응답에 필요한 필드가 없습니다: {missing_fields}"
        )
    
    return data