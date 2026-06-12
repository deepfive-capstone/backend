import os
from dotenv import load_dotenv
from fastapi import HTTPException
from google.oauth2 import id_token
from google.auth.transport import requests
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

load_dotenv()
GOOGLE_CLIENT_ID=os.getenv("GOOGLE_CLIENT_ID")

import urllib.request
import json

def verify_google_token(token: str) -> dict:

    if not GOOGLE_CLIENT_ID:
        raise HTTPException(
            status_code=500,
            detail="Google Client ID가 설정되지 않았습니다."
        )

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
        # id_token 파싱 실패시 access_token으로 간주하고 userinfo API 호출
        try:
            req = urllib.request.Request("https://www.googleapis.com/oauth2/v3/userinfo")
            req.add_header("Authorization", f"Bearer {token}")
            with urllib.request.urlopen(req) as response:
                user_info = json.loads(response.read().decode('utf-8'))
                
                # Google_oauth2 userinfo 반환값에는 email_verified 대신 verified_email (boolean)이 있을 수 있음
                # 하지만 idToken과 형식을 맞추기 위해 확인
                email_verified = user_info.get("email_verified", user_info.get("verified_email", False))
                if not email_verified:
                    raise HTTPException(
                        status_code=401,
                        detail="Google 이메일 인증이 완료되지 않은 계정입니다."
                    )
                # idToken 파서와 같은 구조로 email, name 값을 포함하게 해줌
                return user_info
        except Exception as e:
            raise HTTPException(
                status_code=401,
                detail="유효하지 않은 Google 토큰입니다."
            )