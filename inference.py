from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "running"}

# ✅ MUST be POST (this fixes your error)
@app.post("/reset")
def reset():
    return {"status": "ok"}

@app.post("/predict")
def predict():
    return {"category": "General", "confidence": 0.9}
@app.post("/reset")
def reset():
    print("RESET HIT")   # debug
    return {"status": "ok"}