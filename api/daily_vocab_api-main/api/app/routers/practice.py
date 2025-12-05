from fastapi import APIRouter, HTTPException
from .. import schemas
from ..mock_db import db # เรียกใช้ข้อมูลกลาง
import httpx
import math 
import random

router = APIRouter(prefix="/api", tags=["Practice"])

# URL ของ n8n
N8N_WEBHOOK_URL = "https://ruy888.app.n8n.cloud/webhook-test/39f316ea-5f48-4f4f-8123-b7922ea6cd3c" 

def get_word_difficulty(word: str) -> str:
    word = word.lower()
    advanced = ["serendipity", "ephemeral", "mellifluous", "ubiquitous", "ambivalent"]
    intermediate = ["resilient", "perspective", "ambition", "runway", "construction"]
    if word in advanced: return "Advanced"
    elif word in intermediate: return "Intermediate"
    return "Beginner"

@router.post("/validate-sentence", response_model=schemas.AIResponse)
async def validate_sentence(payload: schemas.SentenceInput):
    sentence = payload.sentence.strip()
    target_word = payload.word_text
    
    # -------------------------------------------------------------
    # 1. ถ้าไม่มีคำศัพท์ -> ปรับตก (ไม่บวกจำนวนครั้ง)
    # -------------------------------------------------------------
    if target_word.lower() not in sentence.lower():
        return {
            "score": 0.0,
            "level": "Beginner",
            "suggestion": f"ได้รับ 0 คะแนน เนื่องจากในประโยคไม่มีคำศัพท์ '{target_word}' ตามโจทย์กำหนด",
            "corrected_sentence": sentence
        }

    # -------------------------------------------------------------
    # 2. ถ้าผ่านด่านแรก -> ถือว่าส่งงานสำเร็จ -> บวกจำนวนครั้งทันที!
    # -------------------------------------------------------------
    db["total_sentences"] += 1  # <--- จุดที่เพิ่ม: บวกเลขตรงนี้!
    
    # -------------------------------------------------------------
    # 3. ส่งไปตรวจ (n8n หรือ Mock)
    # -------------------------------------------------------------
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(N8N_WEBHOOK_URL, json={"word": target_word, "sentence": sentence}, timeout=3.0)
            if response.status_code == 200:
                data = response.json()
                return {
                    "score": data.get("score", 0),
                    "level": data.get("level", "Beginner"),
                    "suggestion": data.get("suggestion", "-"),
                    "corrected_sentence": data.get("corrected_sentence", sentence)
                }
    except:
        pass 

    # Mock Logic
    word_count = len(sentence.split())
    score = 0.0
    score += min(8.0, word_count * 0.8)
    
    difficulty = get_word_difficulty(target_word)
    if difficulty == "Intermediate": score += 1.0
    elif difficulty == "Advanced": score += 2.0
    else: score += 0.5
    
    suggestion = "Good job! You used the vocabulary correctly."
    final_score = min(10.0, round(score, 1))

    if final_score < 5: level = "Beginner"
    elif final_score < 8: level = "Intermediate"
    else: level = "Advanced"

    return {
        "score": final_score,
        "level": level,
        "suggestion": suggestion,
        "corrected_sentence": sentence.capitalize()
    }