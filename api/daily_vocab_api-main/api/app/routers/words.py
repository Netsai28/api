from fastapi import APIRouter
from .. import schemas
import random

router = APIRouter(prefix="/api", tags=["Words"])

@router.get("/word", response_model=schemas.WordResponse)
def get_random_word():
    # Mock Data: สุ่มคำศัพท์ส่งกลับไป
    words_db = [
        {"id": 1, "word": "Serendipity", "meaning": "Happy accident", "difficulty": "Advanced", "part_of_speech": "noun"},
        {"id": 2, "word": "Ephemeral", "meaning": "Short-lived", "difficulty": "Intermediate", "part_of_speech": "adjective"},
        {"id": 3, "word": "Resilient", "meaning": "Recover quickly", "difficulty": "Beginner", "part_of_speech": "adjective"}
    ]
    return random.choice(words_db)