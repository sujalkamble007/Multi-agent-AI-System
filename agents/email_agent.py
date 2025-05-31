"""
Email Agent
- Extracts sender and urgency from email content.
- Flags missing sender as a validation error.
"""


def process_email(content: str):
    """
    Processes an email string, extracts sender and urgency, and returns structured info.
    Flags missing sender as a validation error.

    Args:
        content (str): The raw email content as a string.

    Returns:
        dict: Extracted sender, urgency, raw content, and any validation errors.
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
    result = {
        "sender": sender,
        "urgency": urgency,
        "raw_content": content[:100]  # sample of content
    }
    if not sender:
        result["validation_errors"] = ["Missing sender in email."]
    return result
