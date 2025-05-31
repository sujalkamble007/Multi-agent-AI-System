def process_email(content: str):
    sender = "extracted@example.com"  # mock sender
    urgency = "medium" if "urgent" in content.lower() else "low"
    intent = "RFQ" if "quote" in content.lower() else "Other"

    return {
        "sender": sender,
        "intent": intent,
        "urgency": urgency,
        "content": content
    }
