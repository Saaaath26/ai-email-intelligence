import gradio as gr
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle
import os
from collections import defaultdict

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# ---------- AUTH ----------
def get_gmail_service():
    creds = None

    if os.path.exists('token.pkl'):
        with open('token.pkl', 'rb') as token:
            creds = pickle.load(token)

    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

        with open('token.pkl', 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)

# ---------- FETCH EMAILS ----------
def get_emails(service, max_results=10):
    results = service.users().messages().list(
        userId='me', maxResults=max_results).execute()

    messages = results.get('messages', [])
    emails = []

    for msg in messages:
        msg_data = service.users().messages().get(
            userId='me', id=msg['id']).execute()

        snippet = msg_data.get('snippet', '')
        emails.append(snippet)

    return emails

# ---------- CLASSIFIER ----------
CATEGORY_RULES = {
    "Promotions": ["discount", "sale", "offer"],
    "Social": ["community", "friend", "join"],
    "Tech": ["app", "software", "build"],
    "Events": ["event", "award"],
    "Work": ["meeting", "project"]
}

def classify_email(text):
    text = text.lower()
    scores = defaultdict(int)

    for cat, words in CATEGORY_RULES.items():
        for w in words:
            if w in text:
                scores[cat] += 1

    if scores:
        best = max(scores, key=scores.get)
        return best, 0.8

    return "Other", 0.5

# ---------- MAIN FUNCTION ----------
def fetch_and_classify():
    service = get_gmail_service()
    emails = get_emails(service)

    table = []
    for e in emails:
        cat, conf = classify_email(e)
        table.append([e[:80]+"...", cat, conf])

    return table

# ---------- UI ----------
with gr.Blocks() as demo:
    gr.Markdown("# 📧 AI Email Intelligence")

    btn = gr.Button("Fetch Emails")

    table = gr.Dataframe(
        headers=["Email", "Category", "Confidence"]
    )

    btn.click(fetch_and_classify, outputs=table)

demo.launch()