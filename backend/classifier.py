from collections import defaultdict

CATEGORY_RULES = {
    "Spam": ["win", "free", "click", "offer"],
    "Promotions": ["discount", "sale", "off", "deal", "offer"],
    "Social": ["community", "friend", "join", "connect"],
    "Job": ["job", "hiring", "career", "interview"],
    "Finance": ["bank", "account", "transaction", "payment"],
    "Travel": ["flight", "hotel", "booking", "trip"],
    "Education": ["course", "learn", "training", "study"],
    "Work": ["meeting", "project", "deadline", "client"],
    "Personal": ["family", "party", "invite"],
    "Alerts": ["alert", "warning", "important"],
    "Shopping": ["order", "shipped", "delivery", "amazon"],
    "Events": ["event", "award", "conference"],
    "Tech": ["app", "software", "update", "building"],
    "Support": ["help", "support", "issue"],
    "Notifications": ["notification", "activity", "update"]
}

def classify_email(text):
    text_lower = text.lower()
    scores = defaultdict(int)

    for category, keywords in CATEGORY_RULES.items():
        for word in keywords:
            if word in text_lower:
                scores[category] += 1

    if scores:
        best_category = max(scores, key=scores.get)
        confidence = min(0.7 + 0.1 * scores[best_category], 0.95)
        return best_category, confidence

    if len(text.split()) > 20:
        return "Promotions", 0.6

    return "Personal", 0.6