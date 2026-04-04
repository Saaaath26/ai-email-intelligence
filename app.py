import gradio as gr
import requests
from collections import Counter
import pandas as pd

BASE_URL = "https://ai-email-backend-novs.onrender.com"

def connect_gmail():
    return "👉 Open this link and login:\n" + BASE_URL + "/auth/login"

def get_priority(email):
    text = email["text"].lower()
    if any(word in text for word in ["urgent", "important", "asap"]):
        return "🔥 High"
    elif email["category"] in ["Work", "Finance"]:
        return "⭐ Medium"
    return "Low"

def fetch_emails():
    try:
        response = requests.get(BASE_URL + "/emails")
        data = response.json()

        if "error" in data:
            return [[data["error"], "", "", ""]], [], None, "Login required", pd.DataFrame()

        emails = data.get("emails", [])
        next_token = data.get("next_page_token")

        table = format_table(emails)
        stats, df = generate_stats(emails)

        return table, emails, next_token, stats, df

    except Exception as e:
        return [[str(e), "", "", ""]], [], None, "Error", pd.DataFrame()

def load_more(current_emails, token):
    if not token:
        stats, df = generate_stats(current_emails)
        return format_table(current_emails), current_emails, None, stats, df

    response = requests.get(BASE_URL + "/emails", params={"page_token": token})
    data = response.json()

    new_emails = data.get("emails", [])
    next_token = data.get("next_page_token")

    combined = current_emails + new_emails

    table = format_table(combined)
    stats, df = generate_stats(combined)

    return table, combined, next_token, stats, df

def format_table(emails):
    return [
        [e["text"][:100] + "...", e["category"], get_priority(e), round(e["confidence"], 2)]
        for e in emails
    ]

def generate_stats(emails):
    counter = Counter([e["category"] for e in emails])
    stats_text = "\n".join([f"{k}: {v}" for k, v in counter.items()])

    df = pd.DataFrame({
        "Category": list(counter.keys()),
        "Count": list(counter.values())
    })

    return stats_text, df

def filter_emails(category, emails):
    if category == "All":
        return format_table(emails)
    return format_table([e for e in emails if e["category"] == category])

def export_csv(emails):
    df = pd.DataFrame(emails)
    file_path = "emails.csv"
    df.to_csv(file_path, index=False)
    return file_path

with gr.Blocks() as demo:
    gr.Markdown("# 📧 AI Email Intelligence")

    login_btn = gr.Button("🔐 Connect Gmail")
    fetch_btn = gr.Button("📥 Fetch Emails")
    load_btn = gr.Button("🔄 Load More")
    export_btn = gr.Button("📤 Export CSV")

    status = gr.Textbox()
    dropdown = gr.Dropdown(["All", "Promotions", "Social", "Tech", "Events", "Work"], value="All")

    table = gr.Dataframe(headers=["Email", "Category", "Priority", "Confidence"])
    stats = gr.Textbox()
    chart = gr.BarPlot(x="Category", y="Count")
    file = gr.File()

    state_emails = gr.State([])
    state_token = gr.State(None)

    login_btn.click(connect_gmail, outputs=status)
    fetch_btn.click(fetch_emails, outputs=[table, state_emails, state_token, stats, chart])
    load_btn.click(load_more, inputs=[state_emails, state_token],
                   outputs=[table, state_emails, state_token, stats, chart])
    dropdown.change(filter_emails, inputs=[dropdown, state_emails], outputs=table)
    export_btn.click(export_csv, inputs=state_emails, outputs=file)

demo.launch()