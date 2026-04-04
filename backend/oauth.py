from fastapi import APIRouter
from google_auth_oauthlib.flow import Flow
from fastapi.responses import RedirectResponse
import pickle
import os
import json

router = APIRouter()

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# ⚠️ IMPORTANT: change after deployment
REDIRECT_URI = "http://localhost:8001/auth/callback"

# 🔥 LOAD FROM ENV VARIABLE (RENDER)
client_config = json.loads(os.environ["GOOGLE_CREDENTIALS"])

flow = Flow.from_client_config(
    client_config,
    scopes=SCOPES,
    redirect_uri=REDIRECT_URI,
)

@router.get("/login")
def login():
    auth_url, _ = flow.authorization_url(prompt='consent')
    return RedirectResponse(auth_url)

@router.get("/callback")
def callback(code: str):
    flow.fetch_token(code=code)

    creds = flow.credentials

    with open("token.pkl", "wb") as f:
        pickle.dump(creds, f)

    return {"message": "Login successful + token saved"}