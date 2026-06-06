from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.services.jwt_service import decode_access_token

bearer_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials
    payload = decode_access_token(token)

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="토큰에 사용자 정보가 없습니다."
        )

    user = db.query(User).filter(User.user_id == int(user_id)).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="사용자를 찾을 수 없습니다."
        )

    return user