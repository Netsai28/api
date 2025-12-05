from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://vocabuser:vocabpass123@localhost:3306/vocabulary_db"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_word_by_id(db: Session, word_id: int):
    from app.models import Word
    return db.query(Word).filter(Word.id == word_id).first()