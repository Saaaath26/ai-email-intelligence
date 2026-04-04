from fastapi import FastAPI, Query
from auth import get_gmail_service
from gmail import get_emails
from classifier import classify_email

app = FastAPI()

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

from oauth import router as oauth_router

app.include_router(oauth_router, prefix="/auth")