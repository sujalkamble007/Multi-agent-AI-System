import json

def classify_input(file_content: str, filename: str):
    if filename.lower().endswith(".pdf"):
        format_ = "PDF"
    elif filename.lower().endswith(".json"):
        format_ = "JSON"
    else:
        format_ = "Email"
    
    content_lower = file_content.lower()
    if "quote" in content_lower:
        intent = "RFQ"
    elif "invoice" in content_lower:
        intent = "Invoice"
    elif "complaint" in content_lower:
        intent = "Complaint"
    else:
        intent = "Unknown"

    return format_, intent

def classify_and_route(file_path: str):
    # Read file content depending on type
    if file_path.lower().endswith(".pdf"):
        # For now, just a placeholder text; integrate pdfplumber later
        file_content = "[PDF content extraction not implemented yet]"
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()

    # Classify format + intent
    format_, intent = classify_input(file_content, file_path)

    print(f"Detected Format: {format_}, Intent: {intent}")

    # Route to appropriate agent based on intent
    if format_ == "Email":
        print("Routing to Email Agent...")
        # TODO: call email_agent.process(file_content)
    elif format_ == "JSON":
        print("Routing to JSON Agent...")
        # TODO: call json_agent.process(file_content)
    elif format_ == "PDF":
        print("Routing to PDF Agent...")
        # TODO: call pdf_agent.process(file_content)
    else:
        print("Unknown format. Cannot route.")

    # Return for further processing or logging
    return format_, intent

if __name__ == "__main__":
    # Example test run with a sample file path (adjust path as needed)
    sample_file = "data/sample_email.txt"
    classify_and_route(sample_file)
