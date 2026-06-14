# backend
#실행 전 설정
백엔드 루트 경로에 .env 파일을 생성하고 아래 환경변수를 설정합니다.

DATABASE_URL=mysql+pymysql://계정명:비밀번호@localhost:3306/link_swipe
GOOGLE_CLIENT_ID=Google OAuth Client ID
JWT_SECRET_KEY=JWT Secret Key
JWT_ALGORITHM은 기본값으로 HS256을 사용합니다.

#DB 초기 설정
MySQL 실행 후 아래 SQL 파일을 실행합니다.
sql/init_db.sql
해당 파일은 link_swipe 데이터베이스와 필요한 테이블을 생성합니다.

#서버 실행
python -m uvicorn app.main:app --reload --port 8000
API 문서는 서버 실행 후 아래 주소에서 확인할 수 있습니다.
http://127.0.0.1:8000/docs