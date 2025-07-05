from fastapi import FastAPI
from app.routes import analyze

app = FastAPI()

app.include_router(analyze.router, prefix="/analyze")

@app.get("/")
def home():
    return {"message": "Resume nalysis API is running!"}