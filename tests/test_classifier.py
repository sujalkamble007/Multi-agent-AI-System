import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from agents.classifier_agent import classify_input

def test_classify_email():
    content = "From: test@example.com\nSubject: RFQ\nBody: Please quote."
    format_, intent = classify_input(content, "sample_email.txt")
    assert format_ == "Email"
    assert intent in ["RFQ", "Unknown"]

def test_classify_json():
    content = '{"invoice_id": "INV-1", "date": "2025-01-01", "total_amount": 100.0, "vendor": "Test", "items": ["a"]}'
    format_, intent = classify_input(content, "sample_invoice.json")
    assert format_ == "JSON"
    assert intent in ["Invoice", "Unknown"]

def test_classify_text():
    content = "Quarterly Report Q2 2025\nRevenue: $500,000"
    format_, intent = classify_input(content, "sample_report.txt")
    assert format_ == "Text"
    assert intent in ["RFQ", "Unknown"]
