import pickle
from googleapiclient.discovery import build

def get_gmail_service():
    with open("token.pkl", "rb") as token:
        creds = pickle.load(token)

    service = build('gmail', 'v1', credentials=creds)
    return service