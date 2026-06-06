from pydantic import BaseModel, Field

#프론트->백엔드
class GoogleLoginRequest(BaseModel):
    id_token: str

class UserResponse(BaseModel):
    user_id: int
    email: str
    nickname: str

#JWT 토큰
class LoginResponse(BaseModel):
    access_token: str 
    token_type: str = "bearer"
    user: UserResponse

class NicknameUpdateRequest(BaseModel):
    nickname: str=Field(...,min_length=1, max_length=10)

class MessageResponse(BaseModel):
    message: str