from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pyttsx3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str
    language: str

def speak(text, language):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    if language == "hi-IN" and len(voices) > 1:
        engine.setProperty('voice', voices[1].id)
    else:
        engine.setProperty('voice', voices[0].id)

    engine.say(text)
    engine.runAndWait()

def detect_scam_logic(message):

    msg = message.lower()

    # English scam keywords
    english_keywords = [
        "otp", "one time password", "bank", "bank account",
        "verify", "verification", "click", "link",
        "urgent", "immediately", "update", "kyc",
        "password", "suspend", "account",
        "free", "win", "lottery"
    ]

    # Hindi scam keywords
    hindi_keywords = [
        "ओटीपी", "वन टाइम पासवर्ड", "बैंक", "बैंक खाता",
        "सत्यापित", "सत्यापन", "लिंक",
        "तुरंत", "अभी", "अपडेट", "केवाईसी",
        "पासवर्ड", "खाता", "निलंबित",
        "इनाम", "लॉटरी", "जीत"
    ]

    score = 0

    # English keyword match
    for word in english_keywords:
        if word in msg:
            score += 20

    # Hindi keyword match
    for word in hindi_keywords:
        if word in msg:
            score += 20

    # OTP numeric pattern detection
    if any(char.isdigit() for char in msg) and ("otp" in msg or "ओटीपी" in msg or "one time password" in msg):
        score += 40

    if score > 100:
        score = 100

    scam = score >= 50

    if scam:
        alert_en = "Warning! This message looks like an OTP scam. Do not share OTP."
        alert_hi = "चेतावनी! यह संदेश OTP स्कैम जैसा लगता है। OTP साझा न करें।"
    else:
        alert_en = "Message looks safe."
        alert_hi = "संदेश सुरक्षित है।"

    return {
        "scam": scam,
        "scam_score": score,
        "alert_en": alert_en,
        "alert_hi": alert_hi
    }

@app.get("/")
def home():
    return {"message": "Shield India API Running"}

@app.post("/detect_scam")
def detect_scam(data: Message):

    result = detect_scam_logic(data.message)

    if data.language == "hi-IN":
        speak(result["alert_hi"], "hi-IN")
        alert = result["alert_hi"]
    else:
        speak(result["alert_en"], "en-IN")
        alert = result["alert_en"]

    return {
        "alert": alert,
        "scam_score": result["scam_score"]
    }

@app.post("/check_link")
def check_link(data: dict):
    link = data.get("link", "").lower()

    suspicious = ["bit.ly", "tinyurl", "free", "win", "click"]

    if any(word in link for word in suspicious):
        return {"scam": True, "alert": "⚠️ संदिग्ध फिशिंग लिंक"}
    return {"scam": False, "alert": "✅ लिंक सुरक्षित है"}