from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas
from ..database import get_db
import random

router = APIRouter(prefix="/api", tags=["Words"])

@router.get("/word", response_model=schemas.WordResponse)
def get_random_word(db: Session = Depends(get_db)):
    # 1. พยายามดึงคำศัพท์จาก Database ที่คุณเพิ่ง Seed
    try:
        word_data = db.query(models.Word).order_by(func.random()).first()
        
        if word_data:
            # Map ข้อมูลจาก Database เข้ากับ Schema
            # (ใช้ getattr เพื่อรองรับกรณีชื่อตัวแปรใน models.py ต่างกันเล็กน้อย)
            return {
                "id": word_data.id,
                "word": word_data.word,
                "meaning": getattr(word_data, "definition", getattr(word_data, "meaning", "No meaning found")),
                "difficulty": getattr(word_data, "difficulty_level", getattr(word_data, "difficulty", "Intermediate")),
                "part_of_speech": getattr(word_data, "part_of_speech", "noun")
            }
            
    except Exception as e:
        print(f"⚠️ Database Warning: {e} (Switching to Mock Data)")
        # ถ้ามีปัญหา Database จะไหลลงไปใช้ Mock ด้านล่างอัตโนมัติ

    # 2. Fallback: ข้อมูลสำรอง (ทำงานเมื่อ Database มีปัญหา)
    print("ℹ️ Using Mock Data")
    words_mock = [
        {"id": 1, "word": "Serendipity", "meaning": "Happy accident", "difficulty": "Advanced", "part_of_speech": "noun"},
        {"id": 2, "word": "Ephemeral", "meaning": "Lasting for a very short time", "difficulty": "Advanced", "part_of_speech": "adjective"},
        {"id": 3, "word": "Resilient", "meaning": "Recover quickly", "difficulty": "Intermediate", "part_of_speech": "adjective"},
        {"id": 4, "word": "Runway", "meaning": "A strip of hard ground for aircraft", "difficulty": "Beginner", "part_of_speech": "noun"},
        {"id": 5, "word": "Journey", "meaning": "An act of traveling", "difficulty": "Beginner", "part_of_speech": "noun"}
    ]
    return random.choice(words_mock)