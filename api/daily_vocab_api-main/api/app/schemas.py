from pydantic import BaseModel
from typing import List, Optional

# --- Base Models ---
class WordBase(BaseModel):
    word: str
    meaning: str
    difficulty: str
    part_of_speech: str

class WordResponse(WordBase):
    id: int

# --- Input Models ---
class SentenceInput(BaseModel):
    word_text: str
    sentence: str

# เพิ่มตัวนี้เพื่อกันเหนียว (บางไฟล์อาจเรียกชื่อเก่า)
class ValidateSentenceRequest(SentenceInput):
    pass

# --- Output Models ---
class AIResponse(BaseModel):
    score: float
    level: str
    suggestion: str
    corrected_sentence: str

# เพิ่มตัวนี้เพื่อแก้ Error ที่ไฟล์ words.py เรียกหาชื่อเก่า
class ValidateSentenceResponse(AIResponse):
    pass

class StatItem(BaseModel):
    day: str
    score: float

class DashboardSummary(BaseModel):
    total_sentences: int
    avg_score: float
    streak: int
    history: List[StatItem]