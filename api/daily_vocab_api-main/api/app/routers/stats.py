from fastapi import APIRouter
from .. import schemas
from ..mock_db import db # เรียกใช้ข้อมูลกลาง
import random

router = APIRouter(prefix="/api", tags=["Stats"])

@router.get("/summary", response_model=schemas.DashboardSummary)
def get_dashboard_summary():
    # แค่อ่านค่าจาก db มาแสดง ไม่มีการบวกเพิ่มที่นี่แล้ว
    
    # สุ่มกราฟให้ดูสวยงามเหมือนเดิม
    mock_history = [
        {"day": "Mon", "score": random.uniform(6, 9)},
        {"day": "Tue", "score": random.uniform(7, 10)},
        {"day": "Wed", "score": random.uniform(5, 8)},
        {"day": "Thu", "score": random.uniform(8, 9.5)},
        {"day": "Fri", "score": random.uniform(6, 10)},
    ]

    return {
        "total_sentences": db["total_sentences"], # อ่านค่าล่าสุด
        "avg_score": db["avg_score"],
        "streak": db["streak"],
        "history": mock_history
    }