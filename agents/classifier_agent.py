"""
Classifier Agent
- Detects file format and intent using Hugging Face transformers or fallback keyword logic.
- Routes to the correct agent and returns results.
"""

from transformers.pipelines import pipeline

# Initialize the zero-shot-classification pipeline once
_hf_classifier = None


def get_hf_classifier():
    """
    Loads and returns the Hugging Face zero-shot-classification pipeline.
    Returns None if loading fails.
    """
    global _hf_classifier
    if _hf_classifier is None:
        try:
            _hf_classifier = pipeline(
                "zero-shot-classification", model="facebook/bart-large-mnli"
            )
        except Exception as e:
            print(f"[Classifier Agent] Hugging Face pipeline load failed: {e}")
            _hf_classifier = None
    return _hf_classifier


def classify_input(file_content: str, filename: str):
    """
    Classifies the input file's format and intent.
    Uses LLM if available, otherwise falls back to keyword logic.
    Args:
        file_content (str): The file content as a string.
        filename (str): The file name (used for extension-based detection).
    Returns:
        tuple: (format, intent)
    """
    if filename.lower().endswith(".pdf"):
        format_ = "PDF"
    elif filename.lower().endswith(".json"):
        format_ = "JSON"
    elif filename.lower().endswith(".eml") or "from:" in file_content.lower():
        format_ = "Email"
    else:
        format_ = "Text"

    # Use Hugging Face for intent classification, fallback to improved keyword logic
    try:
        intent = classify_intent_with_llm(file_content)
    except Exception as e:
        print(f"[Classifier Agent] HF model failed ({e}), using keyword fallback.")
        content_lower = file_content.lower()
        if (
            "quote" in content_lower
            or "rfq" in content_lower
            or "request for quote" in content_lower
        ):
            intent = "RFQ"
        elif (
            "invoice" in content_lower
            or "amount" in content_lower
            or "vendor" in content_lower
        ):
            intent = "Invoice"
        elif (
            "complaint" in content_lower
            or "issue" in content_lower
            or "problem" in content_lower
            or "damaged" in content_lower
        ):
            intent = "Complaint"
        elif (
            "order" in content_lower
            or "purchase order" in content_lower
        ):
            intent = "Purchase Order"
        elif (
            "support" in content_lower
            or "help" in content_lower
            or "ticket" in content_lower
        ):
            intent = "Support Ticket"
        else:
            intent = "Unknown"
    return format_, intent


def classify_and_route(file_path: str):
    """
    Reads the file, classifies format and intent, routes to the appropriate agent,
    validates extracted fields, and returns (format, intent, result).
    Args:
        file_path (str): Path to the input file.
    Returns:
        tuple: (format, intent, result dict)
    """
    # Read file content depending on type
    if file_path.lower().endswith(".pdf"):
        try:
            import pdfplumber
            with pdfplumber.open(file_path) as pdf:
                file_content = "\n".join(
                    page.extract_text() or '' for page in pdf.pages
                )
        except Exception as e:
            file_content = (
                "[PDF content extraction failed: {}]".format(e)
            )
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()

    # Classify format + intent
    format_, intent = classify_input(file_content, file_path)

    print(f"Detected Format: {format_}, Intent: {intent}")

    result = None
    validation_errors = []

    # Route to appropriate agent based on intent and format
    if format_ == "Email":
        print("Routing to Email Agent...")
        try:
            from agents.email_agent import process_email
            result = process_email(file_content)
            if not result.get("sender"):
                validation_errors.append("Missing sender in email.")
        except Exception as e:
            result = {"error": f"Email agent failed: {e}"}
    elif format_ == "JSON":
        print("Routing to JSON Agent...")
        try:
            from agents.json_agent import process_json
            result = process_json(file_content)
            if result.get("data") is None:
                validation_errors.append("Invalid or missing invoice data.")
            if result.get("validation_errors"):
                validation_errors.extend(result["validation_errors"])
        except Exception as e:
            result = {"error": f"JSON agent failed: {e}"}
    elif format_ == "PDF" or intent == "Complaint":
        print("Routing to Complaint Agent...")
        try:
            from agents.json_agent import process_complaint
            result = process_complaint(file_content)
            if not result.get("complainant") or not result.get("body"):
                validation_errors.append(
                    "Missing complainant or body in complaint."
                )
        except Exception as e:
            result = {"error": f"Complaint agent failed: {e}"}
    else:
        print("Unknown or unsupported format. Cannot route.")
        result = {"error": "Unknown or unsupported format"}
        validation_errors.append("Unsupported or unknown file format.")

    if validation_errors:
        # If result is not a dict, wrap it in a dict
        if not isinstance(result, dict):
            result = {"error": str(result)}
        # Always convert validation_errors to a string for compatibility
        result["validation_errors"] = ", ".join(validation_errors)

    # Return for further processing or logging
    return format_, intent, result


def classify_intent_with_llm(text):
    """
    Uses Hugging Face zero-shot-classification to determine document intent.
    Returns the top label or 'Unknown'.
    Args:
        text (str): The document text.
    Returns:
        str: The predicted intent label.
    """
    classifier = get_hf_classifier()
    if classifier is None:
        raise RuntimeError("Hugging Face classifier not available")
    labels = ["Invoice", "RFQ", "Complaint", "Regulation"]
    result = classifier(text, labels)
    if isinstance(result, dict) and 'labels' in result:
        return result['labels'][0] if result['labels'] else "Unknown"
    return "Unknown"


if __name__ == "__main__":
    # Example test run with a sample file path (adjust path as needed)
    sample_file = "data/sample_email.txt"
    classify_and_route(sample_file)
