import gradio as gr
import requests
import webbrowser
from collections import Counter
import pandas as pd

BASE_URL = "https://ai-email-backend-novs.onrender.com"

# ---------- LOGIN ----------
def connect_gmail():
    webbrowser.open(BASE_URL + "/auth/login")
    return "✅ Login opened. Complete it in browser."

# ---------- PRIORITY SCORING ----------
def get_priority(email):
    text = email["text"].lower()

    if any(word in text for word in ["urgent", "important", "asap", "deadline"]):
        return "🔥 High"
    elif email["category"] in ["Work", "Finance"]:
        return "⭐ Medium"
    else:
        return "Low"

# ---------- FETCH ----------
def fetch_emails():
    try:
        response = requests.get(BASE_URL + "/emails")
        data = response.json()

        emails = data.get("emails", [])
        next_token = data.get("next_page_token")

        table = format_table(emails)
        stats, df = generate_stats(emails)

        return table, emails, next_token, stats, df

    except Exception as e:
        return [[f"Error: {str(e)}", "", "", ""]], [], None, "Error", pd.DataFrame()

# ---------- LOAD MORE ----------
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

# ---------- FORMAT ----------
def format_table(emails):
    table = []
    for email in emails:
        priority = get_priority(email)

        table.append([
            email["text"][:100] + "...",
            email["category"],
            priority,
            round(email["confidence"], 2)
        ])
    return table

# ---------- FILTER ----------
def filter_emails(category, emails):
    if not emails:
        return []

    if category == "All":
        return format_table(emails)

    filtered = [e for e in emails if e["category"] == category]
    return format_table(filtered)

# ---------- STATS ----------
def generate_stats(emails):
    categories = [e["category"] for e in emails]
    counter = Counter(categories)

    stats_text = "\n".join([f"{k}: {v}" for k, v in counter.items()])

    df = pd.DataFrame({
        "Category": list(counter.keys()),
        "Count": list(counter.values())
    })

    return stats_text, df

# ---------- EXPORT ----------
def export_csv(emails):
    if not emails:
        return "No data"

    df = pd.DataFrame(emails)
    file_path = "emails.csv"
    df.to_csv(file_path, index=False)

    return file_path

# ---------- UI ----------
with gr.Blocks() as demo:

    gr.Markdown("# 📧 AI Email Intelligence Pro Dashboard")
    gr.Markdown("Smart Email Classification + Priority Detection")

    with gr.Row():
        login_btn = gr.Button("🔐 Connect Gmail")
        fetch_btn = gr.Button("📥 Fetch Emails")
        load_btn = gr.Button("🔄 Load More")
        export_btn = gr.Button("📤 Export CSV")

    status = gr.Textbox(label="Status")

    category_dropdown = gr.Dropdown(
        choices=["All", "Promotions", "Social", "Tech", "Events", "Work"],
        value="All",
        label="Filter Category"
    )

    email_table = gr.Dataframe(
        headers=["Email", "Category", "Priority", "Confidence"],
        interactive=False
    )

    stats_box = gr.Textbox(label="📊 Category Stats")

    chart = gr.BarPlot(
        x="Category",
        y="Count",
        title="Email Category Distribution"
    )

    file_output = gr.File(label="Download CSV")

    # STATE
    state_emails = gr.State([])
    state_token = gr.State(None)

    # ---------- EVENTS ----------
    login_btn.click(connect_gmail, outputs=status)

    fetch_btn.click(
        fetch_emails,
        outputs=[email_table, state_emails, state_token, stats_box, chart]
    )

    load_btn.click(
        load_more,
        inputs=[state_emails, state_token],
        outputs=[email_table, state_emails, state_token, stats_box, chart]
    )

    category_dropdown.change(
        filter_emails,
        inputs=[category_dropdown, state_emails],
        outputs=email_table
    )

    export_btn.click(
        export_csv,
        inputs=state_emails,
        outputs=file_output
    )

demo.launch()