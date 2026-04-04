import os
import pickle
from googleapiclient.discovery import build

def get_gmail_service():
    if not os.path.exists("token.pkl"):
        return None

    with open("token.pkl", "rb") as token:
        creds = pickle.load(token)

    return build('gmail', 'v1', credentials=creds)