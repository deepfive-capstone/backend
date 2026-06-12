from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.modules.user import get_current_user
from app.schemas.user import GoogleLoginRequest, LoginResponse, UserResponse, NicknameUpdateRequest, MessageResponse, EmailLoginRequest, SignUpRequest
from app.services.user_service import verify_google_token, verify_password, get_password_hash
from app.services.jwt_service import create_access_token, decode_access_token

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.post("/signup", response_model=LoginResponse)
def signup(
    request: SignUpRequest,
    db: Session = Depends(get_db)
):
    if db.query(User).filter(User.email == request.email).first():
        raise HTTPException(status_code=400, detail="이미 가입된 이메일입니다.")
    
    hashed_password = get_password_hash(request.password)
    user = User(
        email=request.email,
        nickname=request.nickname,
        password_hash=hashed_password,
        provider="email"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    access_token = create_access_token(
        data={
            "sub": str(user.user_id),
            "email": user.email
        }
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "user_id": user.user_id,
            "email": user.email,
            "nickname": user.nickname
        }
    }

@router.post("/login/email", response_model=LoginResponse)
def email_login(
    request: EmailLoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not user.password_hash or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")
    
    access_token = create_access_token(
        data={
            "sub": str(user.user_id),
            "email": user.email
        }
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "user_id": user.user_id,
            "email": user.email,
            "nickname": user.nickname
        }
    }

@router.post("/login/google", response_model=LoginResponse)
def google_login(
    request: GoogleLoginRequest,
    db: Session = Depends(get_db)
):
    # 프론트가 보낸 google token 검증
    google_user = verify_google_token(request.id_token)
    google_sub = google_user["sub"]

    email = google_user["email"]
    nickname = google_user.get("name") or email.split("@")[0]
    user = db.query(User).filter(User.google_sub == google_sub).first()

    # oogle_sub로 못 찾으면 이메일로 한 번 더 조회
    if not user:
        user = db.query(User).filter(User.email == email).first()

        if user:
            user.google_sub = google_sub
            user.provider = "google"

        else:
            # DB에 없는 사용자면 새 회원 생성
            user = User(
                email=email,
                nickname=nickname,
                password_hash=None,
                provider="google",
                google_sub=google_sub
            )

            db.add(user)
        db.commit()
        db.refresh(user)

    # JWT access_token 생성
    access_token = create_access_token(
        data={
            "sub": str(user.user_id),
            "email": user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "user_id": user.user_id,
            "email": user.email,
            "nickname": user.nickname
        }
    }

@router.get("/me", response_model=UserResponse)
def get_my_page(
    current_user: User = Depends(get_current_user)
):
    return {
        "user_id": current_user.user_id,
        "email": current_user.email,
        "nickname": current_user.nickname
    }

@router.patch("/nickname", response_model=UserResponse)
def update_nickname(
    request: NicknameUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    #공백제거
    new_nickname = request.nickname.strip()
    current_user.nickname = new_nickname

    db.commit()
    db.refresh(current_user)

    return {
        "user_id": current_user.user_id,
        "email": current_user.email,
        "nickname": current_user.nickname
    }

@router.post("/logout", response_model=MessageResponse)
def logout(
    current_user: User = Depends(get_current_user)
):
    return{
        "message": "로그아웃 되었습니다."
    }

@router.delete("/me", response_model=MessageResponse)
def delete_accout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db.delete(current_user)
    db.commit()
    return {
        "message": "회원 탈퇴가 완료되었습니다."
    }
