import json

def classify_input(file_content: str, filename: str):
    if filename.endswith(".pdf"):
        format_ = "PDF"
    elif filename.endswith(".json"):
        format_ = "JSON"
    else:
        format_ = "Email"
    
    # Naive intent detection
    if "quote" in file_content.lower():
        intent = "RFQ"
    elif "invoice" in file_content.lower():
        intent = "Invoice"
    elif "complaint" in file_content.lower():
        intent = "Complaint"
    else:
        intent = "Unknown"

    return format_, intent
