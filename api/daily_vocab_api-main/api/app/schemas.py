from pydantic import BaseModel
from typing import List, Optional

# --- สำหรับ Dashboard ---
class StatItem(BaseModel):
    day: str
    score: float

class DashboardSummary(BaseModel):
    total_sentences: int
    avg_score: float
    streak: int
    history: List[StatItem]

# --- สำหรับส่วนอื่นๆ (คงเดิมไว้) ---
class WordBase(BaseModel):
    word: Optional[str] = None
    meaning: Optional[str] = None
    difficulty: Optional[str] = "Beginner"
    part_of_speech: Optional[str] = "noun"

class WordResponse(WordBase):
    id: int
    class Config:
        from_attributes = True

class SentenceInput(BaseModel):
    word_text: str
    sentence: str

class ValidateSentenceRequest(SentenceInput):
    pass

class AIResponse(BaseModel):
    score: float
    level: str
    suggestion: str
    corrected_sentence: str

class ValidateSentenceResponse(AIResponse):
    pass