def process_email(content: str):
    """
    Simple Email Agent stub.
    Extract sender, detect urgency, and return structured info.
    """
    # Naive sender extraction example (look for "From:" line)
    sender = None
    for line in content.splitlines():
        if line.lower().startswith("from:"):
            sender = line.split(":", 1)[1].strip()
            break

    # Naive urgency detection
    urgency = "High" if "urgent" in content.lower() else "Normal"

    # For demo, just print extracted info
    print(f"[Email Agent] Sender: {sender}, Urgency: {urgency}")

    # Return dictionary for logging or further processing
    return {
        "sender": sender,
        "urgency": urgency,
        "raw_content": content[:100]  # sample of content
    }
