import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from fastapi import HTTPException
from jose import jwt, JWTError

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

#토큰 생성
def create_access_token(data: dict) -> str:

    if not JWT_SECRET_KEY:
        raise ValueError("JWT_SECRET_KEY가 .env에 설정되지 않았습니다.")
    
    to_encode = data.copy()

    # 현재 시간 기준으로 만료 시간 계산
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # JWT payload에 만료시간 추가
    to_encode.update({"exp": expire})

    # JWT 생성
    encoded_jwt = jwt.encode(
        to_encode,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )

    return encoded_jwt

#토큰 검증
def decode_access_token(token: str) -> dict:

    if not JWT_SECRET_KEY:
        raise HTTPException(
            status_code=500,
            detail="JWT_SECRET_KEY가 .env에 설정되지 않았습니다."
        )
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
        )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="유효하지 않거나 만료된 토큰입니다."
        )