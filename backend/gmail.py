def get_emails(service, max_results=10, page_token=None):
    results = service.users().messages().list(
        userId='me',
        maxResults=max_results,
        pageToken=page_token
    ).execute()

    messages = results.get('messages', [])
    next_token = results.get('nextPageToken')

    emails = []

    for msg in messages:
        msg_data = service.users().messages().get(
            userId='me', id=msg['id']).execute()

        snippet = msg_data.get('snippet', '')
        emails.append(snippet)

    return emails, next_token