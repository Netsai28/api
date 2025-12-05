from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import practice, stats, words

app = FastAPI()

# ตั้งค่าให้ Frontend (Port 3000) คุยกับ Backend ได้
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# เชื่อมต่อ Router ทั้งหมด
app.include_router(practice.router)
app.include_router(words.router)
app.include_router(stats.router)

@app.get("/")
def read_root():
    return {"message": "Worddee.ai API is running"}