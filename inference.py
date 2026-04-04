from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class EmailRequest(BaseModel):
    text: str = ""

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/reset")
def reset():
    return {"status": "ok"}

@app.post("/predict")
def predict(req: EmailRequest):
    return {"category": "General", "confidence": 0.9}