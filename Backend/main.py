from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class MessageRequest(BaseModel):
    message: str
    language: str


class LinkRequest(BaseModel):
    link: str


# Scam keywords
english_keywords = [
    "bank", "otp", "verify", "account blocked", "click now",
    "urgent", "password", "lottery", "winner", "free money"
]

hindi_keywords = [
    "बैंक", "ओटीपी", "तुरंत", "इनाम", "पासवर्ड",
    "खाता बंद", "क्लिक करें", "लॉटरी"
]


@app.get("/")
def home():
    return {"message": "Shield India API running"}


@app.post("/detect_scam")
def detect_scam(req: MessageRequest):

    text = req.message.lower()

    for word in english_keywords:
        if word in text:
            return {
                "scam": True,
                "alert": "⚠️ This message looks like a scam."
            }

    for word in hindi_keywords:
        if word in text:
            return {
                "scam": True,
                "alert": "⚠️ यह संदेश धोखाधड़ी जैसा लग रहा है।"
            }

    return {
        "scam": False,
        "alert": "✅ Message looks safe."
    }


@app.post("/check_link")
def check_link(req: LinkRequest):

    link = req.link.lower()

    suspicious_domains = [
        "bit.ly",
        "tinyurl",
        "shorturl",
        "grabify",
        "phishing"
    ]

    for domain in suspicious_domains:
        if domain in link:
            return {
                "scam": True,
                "alert": "⚠️ Suspicious shortened link detected!"
            }

    return {
        "scam": False,
        "alert": "✅ Link looks safe."
    }