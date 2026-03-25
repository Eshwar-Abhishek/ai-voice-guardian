from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VoiceInput(BaseModel):
    text: str

# 🔥 Advanced scam detection
HIGH_RISK_PATTERNS = [
    "otp", "one time password", "bank account",
    "credit card", "verify now", "urgent",
    "send money", "transfer", "account blocked",
    "click this link", "update kyc",
    "security code", "login immediately"
]
def detect_scam(text):
    text = text.lower()

    score = 0
    matched = []

    HIGH_RISK_WORDS = [
        "otp", "password", "bank", "account",
        "credit card", "debit card", "cvv",
        "verify", "urgent", "transfer", "money",
        "send", "security code"
    ]

    # count keywords
    for word in HIGH_RISK_WORDS:
        if word in text:
            score += 1
            matched.append(word)

    # 🔥 COMBINATION LOGIC (VERY IMPORTANT)
    if ("otp" in text and "bank" in text):
        score += 3

    if ("otp" in text and ("give" in text or "share" in text)):
        score += 3

    if ("urgent" in text and ("otp" in text or "bank" in text)):
        score += 2

    # 🔥 FINAL DECISION
    if score >= 3:
        return "HIGH RISK", matched
    elif score == 2:
        return "MEDIUM RISK", matched
    else:
        return "LOW RISK", matched

# 🔊 Murf API
MURF_API_KEY = "ap2_f38239de-6d69-4979-8740-e9f2b3214f41"

def generate_voice(text):
    try:
        res = requests.post(
            "https://api.murf.ai/v1/speech/generate",
            headers={
                "api-key": MURF_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "text": text,
                "voiceId": "en-US-natalie"
            }
        )
        return res.json().get("audioFile", "")
    except:
        return ""

@app.post("/analyze")
def analyze(input: VoiceInput):
    risk, words = detect_scam(input.text)

    if risk == "HIGH RISK":
        msg = "⚠️ High risk scam detected! Do NOT share OTP or bank details."
    elif risk == "MEDIUM RISK":
        msg = "⚠️ Suspicious conversation. Stay alert."
    else:
        msg = "✅ Conversation looks safe."

    audio = generate_voice(msg)

    return {
        "risk": risk,
        "keywords": words,
        "message": msg,
        "audio": audio
    }
