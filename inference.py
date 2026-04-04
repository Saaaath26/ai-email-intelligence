from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Request schema (important for proper POST parsing)
class EmailRequest(BaseModel):
    text: str = ""

# Health check (optional but good)
@app.get("/")
def home():
    return {"status": "running"}

# REQUIRED endpoint 1
@app.post("/predict")
def predict(req: EmailRequest):
    text = req.text.lower()

    # simple logic (safe, no dependency issues)
    if "offer" in text or "discount" in text:
        category = "Promotions"
        confidence = 0.9
    elif "meeting" in text or "project" in text:
        category = "Work"
        confidence = 0.85
    elif "friend" in text or "community" in text:
        category = "Social"
        confidence = 0.8
    else:
        category = "General"
        confidence = 0.7

    return {
        "category": category,
        "confidence": confidence
    }

# REQUIRED endpoint 2 (THIS WAS FAILING)
@app.post("/reset")
def reset():
    return {"status": "reset successful"}