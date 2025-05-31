import json
from transformers.pipelines import pipeline
import os

# Initialize the zero-shot-classification pipeline once
_hf_classifier = None

def get_hf_classifier():
    global _hf_classifier
    if _hf_classifier is None:
        try:
            _hf_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        except Exception as e:
            print(f"[Classifier Agent] Hugging Face pipeline load failed: {e}")
            _hf_classifier = None
    return _hf_classifier

def classify_input(file_content: str, filename: str):
    if filename.lower().endswith(".pdf"):
        format_ = "PDF"
    elif filename.lower().endswith(".json"):
        format_ = "JSON"
    else:
        format_ = "Email"
    
    # Use Hugging Face for intent classification, fallback to keyword if model unavailable
    try:
        intent = classify_intent_with_llm(file_content)
    except Exception as e:
        print(f"[Classifier Agent] HF model failed ({e}), using keyword fallback.")
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
        try:
            from agents.email_agent import process_email
            result = process_email(file_content)
        except Exception as e:
            result = {"error": f"Email agent failed: {e}"}
    elif format_ == "JSON":
        print("Routing to JSON Agent...")
        try:
            from agents.json_agent import process_json
            result = process_json(file_content)
        except Exception as e:
            result = {"error": f"JSON agent failed: {e}"}
    elif format_ == "PDF":
        print("Routing to PDF Agent...")
        result = {"message": "PDF agent not implemented yet"}
    else:
        print("Unknown format. Cannot route.")
        result = {"error": "Unknown format"}

    # Return for further processing or logging
    return format_, intent, result

def classify_intent_with_llm(text):
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
