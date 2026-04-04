from fastapi import APIRouter
from google_auth_oauthlib.flow import Flow
from fastapi.responses import RedirectResponse
import pickle

router = APIRouter()

CLIENT_SECRETS_FILE = "credentials.json"
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
REDIRECT_URI = "http://localhost:8001/auth/callback"

flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
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

    # 🔥 SAVE TOKEN
    with open("token.pkl", "wb") as f:
        pickle.dump(creds, f)

    return {"message": "Login successful + token saved"}