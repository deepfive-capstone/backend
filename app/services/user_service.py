import os
from dotenv import load_dotenv
from fastapi import HTTPException
from google.oauth2 import id_token
from google.auth.transport import requests

load_dotenv()
GOOGLE_CLIENT_ID=os.getenv("GOOGLE_CLIENT_ID")

def verify_google_token(token: str) -> dict:
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(
            status_code=500,
            detail="Google Client ID가 설정되지 않았습니다."
        )
    
    #테스트용
    if token == "test":
        return {
            "sub": "test-google-sub-123",
            "email": "test@gmail.com",
            "email_verified": True,
            "name": "테스트유저",
            "picture": None,
        }
    
    try:
        account_info = id_token.verify_oauth2_token(
            token, 
            requests.Request(),
            GOOGLE_CLIENT_ID
        )
        if account_info.get("iss") not in [
            "accounts.google.com",
            "https://accounts.google.com"
        ]:
            raise HTTPException(
                status_code=401,
                detail="Google에서 발급한 토큰이 아닙니다."
            )
    
        if not account_info.get("email_verified"):
            raise HTTPException(
                status_code=401,
                detail="Google 이메일 인증이 완료되지 않은 계정입니다."
            )
        return account_info
    
    except ValueError:
        # 토큰이 위조되었거나, 만료되었을 때
        raise HTTPException(
            status_code=401,
            detail="유효하지 않은 Google id_token입니다."
        )