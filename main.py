import os
import re
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ----------------------------
# APP INIT
# ----------------------------
app = FastAPI(title="AI Voice Guardian PRO")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# ENV (SAFE)
# ----------------------------
MURF_API_KEY = os.getenv("ap2_76ae0343-204d-49fd-9951-656698a34c8a")

# ----------------------------
# INPUT MODEL
# ----------------------------
class UserInput(BaseModel):
    text: str

# ----------------------------
# NORMALIZE
# ----------------------------
def normalize(text):
    return text.lower().strip()

# ----------------------------
# SMART RISK ANALYSIS
# ----------------------------
def analyze_text(text):
    score = 0
    categories = []
    explanation = []

    patterns = {
        "Financial Scam": [
            "otp", "password", "bank", "upi", "transfer", "money", "pin"
        ],
        "Phishing": [
            "link", "click", "verify", "login", "account"
        ],
        "Grooming": [
            "secret", "don't tell", "meet alone", "private"
        ],
        "Urgency Pressure": [
            "urgent", "hurry", "now", "immediately", "jaldi"
        ],
        "Scam Offer": [
            "lottery", "prize", "win", "free", "offer"
        ]
    }

    for category, words in patterns.items():
        matches = sum(1 for word in words if re.search(rf"\b{re.escape(word)}\b", text))
        if matches > 0:
            categories.append(category)
            score += matches * 20
            explanation.append(f"{category} indicators detected")

    # contextual intelligence
    if "send" in text and "money" in text:
        score += 20
        categories.append("Financial Scam")
        explanation.append("Request to send money detected")

    if "share" in text and "details" in text:
        score += 20
        categories.append("Phishing")
        explanation.append("Request for sensitive details detected")

    score = min(score, 100)

    return score, list(set(categories)), explanation

# ----------------------------
# HUMAN-LIKE RESPONSE
# ----------------------------
def generate_response(risk, categories, explanation):
    if risk > 70:
        return (
            f"This sounds dangerous. Risk level is {risk} percent. "
            f"कृपया तुरंत रुकें और किसी trusted adult को बताएं."
        )

    elif risk > 40:
        return (
            f"This might be unsafe. Risk level is {risk} percent. "
            f"सावधान रहें और सोच समझकर आगे बढ़ें."
        )

    else:
        return (
            f"This seems safe. Risk level is {risk} percent. "
            f"सब सुरक्षित लग रहा है लेकिन सतर्क रहें."
        )

# ----------------------------
# MURF VOICE
# ----------------------------
def generate_voice(text):
    if not MURF_API_KEY:
        print("⚠️ Missing Murf API key")
        return None

    try:
        response = requests.post(
            "https://api.murf.ai/v1/speech/generate",
            json={
                "text": text,
                "voiceId": "en-US-natalie",
                "format": "mp3"
            },
            headers={
                "api-key": MURF_API_KEY,
                "Content-Type": "application/json"
            },
            timeout=10
        )

        print("MURF STATUS:", response.status_code)

        if response.status_code != 200:
            print("MURF ERROR:", response.text)
            return None

        data = response.json()

        # handle multiple formats
        if "audioFile" in data:
            return data["audioFile"]
        elif "data" in data and "audioFile" in data["data"]:
            return data["data"]["audioFile"]

        return None

    except Exception as e:
        print("VOICE ERROR:", str(e))
        return None

# ----------------------------
# MAIN API
# ----------------------------
@app.post("/process")
def process_input(user: UserInput):
    try:
        text = normalize(user.text)

        risk_score, categories, explanation = analyze_text(text)

        response_text = generate_response(risk_score, categories, explanation)

        audio_url = generate_voice(response_text)

        print("INPUT:", text)
        print("RISK:", risk_score)
        print("CATEGORIES:", categories)

        return {
            "response": response_text,
            "risk": risk_score,
            "categories": categories,
            "explanation": explanation,
            "audio": audio_url
        }

    except Exception as e:
        print("SERVER ERROR:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")