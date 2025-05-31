import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from agents.email_agent import process_email
from agents.json_agent import process_json, process_complaint

# Email Agent Tests
def test_process_email_valid():
    content = "From: test@example.com\nSubject: Test\nBody: Hello!"
    result = process_email(content)
    assert result["sender"] == "test@example.com"
    assert result["urgency"] == "Normal"
    assert "raw_content" in result
    assert "validation_errors" not in result

def test_process_email_missing_sender():
    content = "Subject: Test\nBody: Hello!"
    result = process_email(content)
    assert result["sender"] is None
    assert "validation_errors" in result

# JSON Agent Tests
def test_process_json_valid():
    content = '{"invoice_id": "INV-1", "date": "2025-01-01", "total_amount": 100.0, "vendor": "Test", "items": ["a"]}'
    result = process_json(content)
    assert result["data"]["invoice_id"] == "INV-1"
    assert result["errors"] is None

def test_process_json_invalid_json():
    content = '{invalid json}'
    result = process_json(content)
    assert "error" in result

def test_process_json_missing_field():
    content = '{"date": "2025-01-01", "total_amount": 100.0, "vendor": "Test", "items": ["a"]}'
    result = process_json(content)
    assert result["data"] is None
    assert result["errors"] is not None

# Complaint Agent Tests
def test_process_complaint_valid():
    content = "From: user@x.com\nSubject: Issue\nBody: Something broke."
    result = process_complaint(content)
    assert result["complainant"] == "user@x.com"
    assert result["subject"] == "Issue"
    assert result["body"] == "Something broke."

def test_process_complaint_missing_fields():
    content = "Subject: Issue\nBody: Something broke."
    result = process_complaint(content)
    assert result["complainant"] is None
    assert result["subject"] == "Issue"
    assert result["body"] == "Something broke."
