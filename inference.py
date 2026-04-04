from fastapi import FastAPI
from pydantic import BaseModel
from backend.classifier import classify_email

app = FastAPI()

class EmailRequest(BaseModel):
    text: str

@app.post("/predict")
def predict(req: EmailRequest):
    category, confidence = classify_email(req.text)
    return {
        "category": category,
        "confidence": confidence
    }

@app.post("/reset")
def reset():
    return {"message": "reset successful"}