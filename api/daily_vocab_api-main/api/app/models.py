from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from sqlalchemy.sql import func
from .database import Base

class Word(Base):
    __tablename__ = "words"
    
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, unique=True, nullable=False)
    
    # ⚠️ จุดสำคัญ: ต้องชื่อ definition ตรงกับ seed_direct.py
    definition = Column(Text) 
    
    # ⚠️ จุดสำคัญ: ต้องชื่อ difficulty_level ตรงกับ seed_direct.py
    difficulty_level = Column(String, default='Beginner')
    
    part_of_speech = Column(String, default='noun')
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PracticeSubmission(Base):
    __tablename__ = "practice_submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, default=1)
    word_id = Column(Integer, nullable=False)
    submitted_sentence = Column(Text, nullable=False)
    score = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())