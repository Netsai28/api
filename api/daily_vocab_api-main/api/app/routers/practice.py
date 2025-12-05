from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db
import httpx
import random

router = APIRouter(tags=["Practice"])

# 🔴 URL ของ n8n (ตรวจสอบให้แน่ใจว่า Workflow ใน n8n กำลังกด Execute รออยู่ หรือ Activate แล้ว)
N8N_WEBHOOK_URL = "https://ruy888.app.n8n.cloud/webhook-test/39f316ea-5f48-4f4f-8123-b7922ea6cd3c"

@router.post("/validate-sentence", response_model=schemas.ValidateSentenceResponse)
async def validate_sentence(payload: schemas.ValidateSentenceRequest, db: Session = Depends(get_db)):
    print(f"🚀 Sending to n8n: Word='{payload.word_text}', Sentence='{payload.sentence}'")
    
    # 1. ดึงข้อมูลคำศัพท์
    word_item = db.query(models.Word).filter(models.Word.word == payload.word_text).first()
    word_id = word_item.id if word_item else 0
    difficulty = word_item.difficulty_level if word_item else "Beginner"

    ai_result = {}

    # 2. เชื่อมต่อ n8n (AI)
    try:
        async with httpx.AsyncClient() as client:
            # เพิ่ม timeout 30 วินาที (เผื่อ AI คิดนาน)
            response = await client.post(
                N8N_WEBHOOK_URL,
                json={
                    "sentence": payload.sentence,
                    "word": payload.word_text,
                    "difficulty": difficulty  # ส่งระดับความยากไปด้วย เพื่อให้ AI ปรับเกณฑ์คะแนน
                },
                timeout=30.0 
            )
        
        # เช็คว่า n8n ตอบกลับมาจริงไหม
        if response.status_code == 200:
            data = response.json()
            print(f"✅ n8n Response: {data}") # ดู Log ตรงนี้ว่า n8n ตอบอะไรกลับมา

            # ตรวจสอบว่า n8n ส่งคะแนนมาเป็นตัวเลขหรือไม่
            raw_score = data.get("score", 0)
            if isinstance(raw_score, str):
                try:
                    score = float(raw_score)
                except:
                    score = 0.0
            else:
                score = float(raw_score)

            ai_result = {
                "score": score,
                "level": data.get("level", difficulty),
                "suggestion": data.get("suggestion", "Good job! (No suggestion from AI)"),
                "corrected_sentence": data.get("corrected_sentence", payload.sentence)
            }
        else:
            print(f"❌ n8n Error Status: {response.status_code}")
            print(f"❌ n8n Body: {response.text}")
            raise Exception("n8n responded with error")

    except Exception as e:
        print(f"⚠️ Connection Failed: {e}")
        print("⚠️ --> Using Fallback Mock Data (คะแนนจะไม่ตรงความเป็นจริง)")
        
        # Mock คะแนนแก้ขัด (กรณีต่อ AI ไม่ติดจริงๆ)
        ai_result = {
            "score": 5.0,
            "level": difficulty,
            "suggestion": "System could not connect to AI. Please check n8n Webhook.",
            "corrected_sentence": payload.sentence
        }

    # 3. บันทึกลง Database
    try:
        new_submission = models.PracticeSubmission(
            user_id=1,
            word_id=word_id,
            submitted_sentence=payload.sentence,
            score=ai_result["score"]
        )
        db.add(new_submission)
        db.commit()
        db.refresh(new_submission)
    except Exception as db_err:
        print(f"❌ Database Error: {db_err}")

    return ai_result