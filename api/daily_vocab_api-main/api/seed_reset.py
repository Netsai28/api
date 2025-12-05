import sys
import os

# --- 1. แก้ปัญหา Import (สำคัญมาก) ---
# สั่งให้ Python รู้จักโฟลเดอร์ปัจจุบัน เพื่อให้หา 'app' เจอ
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine
from app import models

# --- 2. สร้างตารางใน Database ใหม่ ---
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

# --- 3. ข้อมูลคำศัพท์ 50 คำ ---
initial_words = [
    {"word": "Serendipity", "definition": "The occurrence of events by chance in a happy way.", "difficulty_level": "Advanced"},
    {"word": "Petrichor", "definition": "A pleasant smell that frequently accompanies the first rain after a long period of warm, dry weather.", "difficulty_level": "Advanced"},
    {"word": "Ephemeral", "definition": "Lasting for a very short time.", "difficulty_level": "Advanced"},
    {"word": "Resilience", "definition": "The capacity to recover quickly from difficulties.", "difficulty_level": "Intermediate"},
    {"word": "Journey", "definition": "An act of traveling from one place to another.", "difficulty_level": "Beginner"},
    {"word": "Create", "definition": "Bring something into existence.", "difficulty_level": "Beginner"},
    {"word": "Dream", "definition": "A series of thoughts, images, and sensations occurring in a person's mind during sleep.", "difficulty_level": "Beginner"},
    {"word": "Explore", "definition": "Travel in or through (an unfamiliar country or area) in order to learn about it.", "difficulty_level": "Beginner"},
    {"word": "Victory", "definition": "An act of defeating an enemy or opponent in a battle, game, or other competition.", "difficulty_level": "Intermediate"},
    {"word": "Memory", "definition": "Something remembered from the past.", "difficulty_level": "Beginner"},
    {"word": "Ambition", "definition": "A strong desire to do or to achieve something.", "difficulty_level": "Intermediate"},
    {"word": "Harmony", "definition": "The quality of forming a pleasing and consistent whole.", "difficulty_level": "Intermediate"},
    {"word": "Courage", "definition": "The ability to do something that frightens one.", "difficulty_level": "Intermediate"},
    {"word": "Freedom", "definition": "The power or right to act, speak, or think as one wants.", "difficulty_level": "Intermediate"},
    {"word": "Kindness", "definition": "The quality of being friendly, generous, and considerate.", "difficulty_level": "Beginner"},
]

print("🌱 Starting database seed...")

count = 0
for item in initial_words:
    existing = db.query(models.Word).filter(models.Word.word == item["word"]).first()
    if not existing:
        new_word = models.Word(
            word=item["word"],
            definition=item["definition"],
            difficulty_level=item["difficulty_level"]
        )
        db.add(new_word)
        count += 1
        print(f"   [+] Added: {item['word']}")
    else:
        print(f"   [x] Skipped (Exists): {item['word']}")

db.commit()
print(f"\n✅ Successfully added {count} new words!")
print(f"📊 Total words in DB: {db.query(models.Word).count()}")
db.close()