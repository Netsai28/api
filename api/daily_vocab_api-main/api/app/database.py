from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# หาตำแหน่งไฟล์ vocabulary.db แบบเจาะจง (Absolute Path)
# ถอยจากโฟลเดอร์ app ออกมา 1 ชั้น
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "vocabulary.db")

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# print(f"📂 Database connected at: {DB_PATH}")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()