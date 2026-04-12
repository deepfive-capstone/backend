from fastapi import FastAPI
from app.routers import content

app = FastAPI()

app.include_router(content.router)

@app.get("/")
def read_root():
    return{"message": "Backend is running!"}
