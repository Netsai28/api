from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import random
import httpx

app = FastAPI()

# อนุญาตให้ Frontend เชื่อมต่อ
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock Database
fake_db = {"total_sentences": 42, "streak": 5, "avg_score": 7.8}

# Data Models
class SentenceInput(BaseModel):
    word_text: str
    sentence: str

class WordResponse(BaseModel):
    id: int
    word: str
    meaning: str
    difficulty: str
    part_of_speech: str

class DashboardSummary(BaseModel):
    total_sentences: int
    avg_score: float
    streak: int
    history: List[dict]

class AIResponse(BaseModel):
    score: float
    level: str
    suggestion: str
    corrected_sentence: str

# API: ดึงคำศัพท์
@app.get("/api/word", response_model=WordResponse)
def get_random_word():
    words_db = [
        {"id": 1, "word": "Serendipity", "meaning": "Happy accident", "difficulty": "Advanced", "part_of_speech": "noun"},
        {"id": 2, "word": "Runway", "meaning": "A strip of hard ground for aircraft", "difficulty": "Beginner", "part_of_speech": "noun"},
        {"id": 3, "word": "Resilient", "meaning": "Recover quickly", "difficulty": "Intermediate", "part_of_speech": "adjective"},
        {"id": 4, "word": "Ephemeral", "meaning": "Lasting for a very short time", "difficulty": "Advanced", "part_of_speech": "adjective"}
    ]
    return random.choice(words_db)

# API: ตรวจสอบประโยค
N8N_URL = "https://ruy888.app.n8n.cloud/webhook-test/39f316ea-5f48-4f4f-8123-b7922ea6cd3c"

@app.post("/api/validate-sentence", response_model=AIResponse)
async def validate_sentence(payload: SentenceInput):
    if payload.word_text.lower() not in payload.sentence.lower():
        return {
            "score": 0.0,
            "level": "Beginner",
            "suggestion": f"Missing word '{payload.word_text}'",
            "corrected_sentence": payload.sentence
        }
    
    fake_db["total_sentences"] += 1

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(N8N_URL, json={"word": payload.word_text, "sentence": payload.sentence}, timeout=5.0)
            if resp.status_code == 200:
                data = resp.json()
                return {
                    "score": data.get("score", 0),
                    "level": data.get("level", "Beginner"),
                    "suggestion": data.get("suggestion", "-"),
                    "corrected_sentence": data.get("corrected_sentence", payload.sentence)
                }
    except:
        pass

    # Mock Fallback
    return {
        "score": 8.5,
        "level": "Intermediate",
        "suggestion": "Good job! (Offline Mode)",
        "corrected_sentence": payload.sentence.capitalize()
    }

# API: Dashboard
@app.get("/api/summary", response_model=DashboardSummary)
def get_dashboard_summary():
    mock_history = [
        {"day": "Mon", "score": 8}, {"day": "Tue", "score": 7}, {"day": "Wed", "score": 9},
        {"day": "Thu", "score": 6}, {"day": "Fri", "score": 8}, {"day": "Sat", "score": 7}, {"day": "Sun", "score": 9}
    ]
    return {
        "total_sentences": fake_db["total_sentences"],
        "avg_score": fake_db["avg_score"],
        "streak": fake_db["streak"],
        "history": mock_history
    }