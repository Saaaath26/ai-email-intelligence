from fastapi import FastAPI, Query
from backend.oauth import router as oauth_router
from backend.auth import get_gmail_service
from backend.gmail import get_emails
from backend.classifier import classify_email

app = FastAPI()

# OAuth routes
app.include_router(oauth_router, prefix="/auth")


@app.get("/")
def root():
    return {"message": "Backend running"}


@app.get("/emails")
def read_emails(page_token: str = Query(default=None)):
    service = get_gmail_service()
    emails, next_token = get_emails(service, page_token=page_token)

    results = []
    for email in emails:
        label, score = classify_email(email)
        results.append({
            "text": email,
            "category": label,
            "confidence": float(score)
        })

    return {
        "emails": results,
        "next_page_token": next_token
    }