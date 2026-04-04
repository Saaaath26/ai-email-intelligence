from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class EmailRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "API running"}

@app.post("/predict")
def predict(req: EmailRequest):
    text = req.text.lower()

    if "offer" in text or "discount" in text:
        return {"category": "Promotions", "confidence": 0.9}
    elif "meeting" in text or "project" in text:
        return {"category": "Work", "confidence": 0.85}
    elif "friend" in text:
        return {"category": "Social", "confidence": 0.8}

    return {"category": "General", "confidence": 0.7}

@app.post("/reset")
def reset():
    return {"status": "reset done"}