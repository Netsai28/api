from fastapi import APIRouter
from .. import schemas
from ..mock_db import db 
import random

router = APIRouter(prefix="/api", tags=["Stats"])

@router.get("/summary", response_model=schemas.DashboardSummary)
def get_dashboard_summary():
    # Mock กราฟครบ 7 วัน (Mon-Sun)
    mock_history = [
        {"day": "Mon", "score": random.uniform(5, 8)},
        {"day": "Tue", "score": random.uniform(6, 9)},
        {"day": "Wed", "score": random.uniform(4, 7)},
        {"day": "Thu", "score": random.uniform(7, 10)},
        {"day": "Fri", "score": random.uniform(8, 9.5)},
        {"day": "Sat", "score": random.uniform(3, 6)},
        {"day": "Sun", "score": random.uniform(9, 10)},
    ]

    return {
        "total_sentences": db["total_sentences"], 
        "avg_score": round(random.uniform(7.5, 9.0), 1),
        "streak": db["streak"],
        "history": mock_history # ส่งข้อมูลกราฟ 7 วันกลับไป
    }