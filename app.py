import gradio as gr
import requests
from collections import Counter
import pandas as pd

BASE_URL = "https://ai-email-backend-novs.onrender.com"

# ---------- LOGIN ----------
def connect_gmail():
    return f"<a href='{BASE_URL}/auth/login' target='_blank'>🔐 Click here to login with Gmail</a>"

# ---------- PRIORITY ----------
def get_priority(email):
    text = email["text"].lower()
    if any(word in text for word in ["urgent", "important", "asap"]):
        return "🔥 High"
    elif email["category"] in ["Work", "Finance"]:
        return "⭐ Medium"
    return "Low"

# ---------- CATEGORY COLOR ----------
def get_color(category):
    colors = {
        "Promotions": "🟡",
        "Social": "🔵",
        "Tech": "🟣",
        "Events": "🟢",
        "Work": "🔴"
    }
    return colors.get(category, "⚪")

# ---------- FETCH ----------
def fetch_emails():
    try:
        res = requests.get(BASE_URL + "/emails")
        data = res.json()

        if "error" in data:
            return [], [], None, "⚠️ Please login first", pd.DataFrame()

        emails = data["emails"]
        token = data["next_page_token"]

        table = format_table(emails)
        stats, df = generate_stats(emails)

        return table, emails, token, stats, df

    except Exception as e:
        return [], [], None, str(e), pd.DataFrame()

# ---------- LOAD MORE ----------
def load_more(current, token):
    if not token:
        stats, df = generate_stats(current)
        return format_table(current), current, None, stats, df

    res = requests.get(BASE_URL + "/emails", params={"page_token": token})
    data = res.json()

    new = data["emails"]
    token = data["next_page_token"]

    combined = current + new

    table = format_table(combined)
    stats, df = generate_stats(combined)

    return table, combined, token, stats, df

# ---------- FORMAT ----------
def format_table(emails):
    rows = []
    for e in emails:
        rows.append([
            e["text"][:90] + "...",
            f"{get_color(e['category'])} {e['category']}",
            get_priority(e),
            round(e["confidence"], 2)
        ])
    return rows

# ---------- STATS ----------
def generate_stats(emails):
    counter = Counter([e["category"] for e in emails])

    stats = " | ".join([f"{k}: {v}" for k, v in counter.items()])

    df = pd.DataFrame({
        "Category": list(counter.keys()),
        "Count": list(counter.values())
    })

    return stats, df

# ---------- FILTER ----------
def filter_emails(cat, emails):
    if cat == "All":
        return format_table(emails)
    return format_table([e for e in emails if e["category"] == cat])

# ---------- EXPORT ----------
def export_csv(emails):
    df = pd.DataFrame(emails)
    file = "emails.csv"
    df.to_csv(file, index=False)
    return file

# ---------- UI ----------
with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue")) as demo:

    gr.Markdown("""
    # 🚀 AI Email Intelligence
    ### Smart Inbox. Clean Insights. Instant Priority.
    """)

    with gr.Row():
        login_btn = gr.Button("🔐 Connect Gmail", variant="primary")
        fetch_btn = gr.Button("📥 Fetch Emails")
        load_btn = gr.Button("🔄 Load More")
        export_btn = gr.Button("📤 Export")

    status = gr.HTML()

    with gr.Row():
        dropdown = gr.Dropdown(
            ["All", "Promotions", "Social", "Tech", "Events", "Work"],
            value="All",
            label="🎯 Filter"
        )

    with gr.Row():
        email_table = gr.Dataframe(
            headers=["📧 Email", "🏷 Category", "⭐ Priority", "📊 Confidence"],
            interactive=False,
            wrap=True
        )

    with gr.Row():
        stats_box = gr.Markdown("📊 **Stats will appear here**")

    with gr.Row():
        chart = gr.BarPlot(
            x="Category",
            y="Count",
            title="📊 Email Distribution"
        )

    file = gr.File()

    # STATE
    state_emails = gr.State([])
    state_token = gr.State(None)

    # EVENTS
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

    dropdown.change(
        filter_emails,
        inputs=[dropdown, state_emails],
        outputs=email_table
    )

    export_btn.click(export_csv, inputs=state_emails, outputs=file)

demo.launch()