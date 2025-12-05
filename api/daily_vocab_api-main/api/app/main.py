from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import httpx
import random
from datetime import datetime

app = FastAPI(title="Worddee.ai Final")

# --- Config ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 💾 Database จำลอง ---
# เริ่มต้นเป็น 0 ทั้งหมด เพื่อรอการนับจริง (กราฟจะว่างเปล่าตอนเริ่ม)
fake_db = {
    "total_sentences": 0,
    "streak": 0,
    "avg_score": 0.0,
    "history": [
        {"day": "Mon", "score": 0},
        {"day": "Tue", "score": 0},
        {"day": "Wed", "score": 0},
        {"day": "Thu", "score": 0},
        {"day": "Fri", "score": 0},
        {"day": "Sat", "score": 0},
        {"day": "Sun", "score": 0},
    ]
}

# --- Data Models ---
class SentenceInput(BaseModel):
    word_text: str
    sentence: str

class WordResponse(BaseModel):
    id: int
    word: str
    meaning: str
    difficulty: str
    part_of_speech: str

class AIResponse(BaseModel):
    score: float
    level: str
    suggestion: str
    corrected_sentence: str

class StatItem(BaseModel):
    day: str
    score: float

class DashboardSummary(BaseModel):
    total_sentences: int
    avg_score: float
    streak: int
    history: List[StatItem]

# --- 1. API ดึงคำศัพท์ ---
@app.get("/api/word", response_model=WordResponse)
def get_random_word():
    words_db = [
        {"id": 1, "word": "Serendipity", "meaning": "Happy accident", "difficulty": "Advanced", "part_of_speech": "noun"},
        {"id": 2, "word": "Runway", "meaning": "A strip of hard ground for aircraft", "difficulty": "Beginner", "part_of_speech": "noun"},
        {"id": 3, "word": "Resilient", "meaning": "Recover quickly", "difficulty": "Intermediate", "part_of_speech": "adjective"},
        {"id": 4, "word": "Establish", "meaning": "Set up on a firm basis", "difficulty": "Intermediate", "part_of_speech": "verb"},
        {"id": 5, "word": "Journey", "meaning": "An act of traveling", "difficulty": "Beginner", "part_of_speech": "noun"},
        {"id": 6, "word": "Ephemeral", "meaning": "Lasting for a very short time", "difficulty": "Advanced", "part_of_speech": "adjective"}
    ]
    return random.choice(words_db)

# --- 2. API ตรวจประโยค + นับจำนวนครั้ง + Feedback จริง ---
N8N_URL = "https://ruy888.app.n8n.cloud/webhook-test/39f316ea-5f48-4f4f-8123-b7922ea6cd3c"

@app.post("/api/validate-sentence", response_model=AIResponse)
async def validate_sentence(payload: SentenceInput):
    # 2.1 กฎเหล็ก
    if payload.word_text.lower() not in payload.sentence.lower():
        return {
            "score": 0.0,
            "level": "Beginner",
            "suggestion": f"You must use the word '{payload.word_text}' in your sentence.",
            "corrected_sentence": payload.sentence
        }

    # -------------------------------------------------------
    # ✅ Logic นับจำนวนครั้ง (Frequency)
    # -------------------------------------------------------
    
    # 1. บวกยอดรวม
    fake_db["total_sentences"] += 1
    
    # 2. หาวันปัจจุบัน (เช่น "Sat")
    today_short = datetime.now().strftime("%a") 
    
    # 3. วนลูปหาแท่งกราฟของวันนี้ แล้วบวกเพิ่มทีละ 1
    for item in fake_db["history"]:
        if item["day"] == today_short:
            item["score"] += 1  # 👈 จุดสำคัญ: บวก 1 ทันทีที่กดส่ง
            break

    # -------------------------------------------------------

    final_score = 0.0
    suggestion = ""
    level = "Beginner"

    # Logic ตรวจคำตอบ (n8n / Mock)
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(N8N_URL, json={"word": payload.word_text, "sentence": payload.sentence}, timeout=10.0)
            if resp.status_code == 200:
                data = resp.json()
                return {
                    "score": data.get("score", 0),
                    "level": data.get("level", "Beginner"),
                    "suggestion": data.get("suggestion", "No suggestion"),
                    "corrected_sentence": data.get("corrected_sentence", payload.sentence)
                }
    except:
        pass

    # Mock (Offline) - คำนวณคะแนนจริง
    final_score = round(min(10.0, len(payload.sentence.split()) * 0.8), 1)
    
    # ✅ Logic เลือกคำแนะนำตามคะแนน (ไม่ใช้ Offline Mode แล้ว)
    if final_score < 5.0:
        level = "Beginner"
        suggestions = [
            "Your sentence is a bit short. Try adding more details.",
            "Good start! Can you expand it with adjectives?",
            "Try to make a complete sentence with subject and verb."
        ]
    elif final_score < 8.0:
        level = "Intermediate"
        suggestions = [
            "Nice sentence! You are using the vocabulary correctly.",
            "Good structure. Try making it more complex for a higher score.",
            "Well done! Adding more context would be perfect."
        ]
    else:
        level = "Advanced"
        suggestions = [
            "Excellent work! Your sentence is rich and meaningful.",
            "Perfect usage! You have mastered this word.",
            "Outstanding! This is a high-quality sentence."
        ]
    
    suggestion = random.choice(suggestions)

    return {
        "score": final_score,
        "level": level,
        "suggestion": suggestion,
        "corrected_sentence": payload.sentence.capitalize()
    }

# --- 3. API Dashboard ---
@app.get("/api/summary", response_model=DashboardSummary)
def get_dashboard_summary():
    return {
        "total_sentences": fake_db["total_sentences"],
        "avg_score": fake_db["avg_score"], # (อาจจะไม่ได้ใช้อันนี้แล้วในกราฟแบบนับจำนวน)
        "streak": fake_db["streak"],
        "history": fake_db["history"]
    }