import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import subprocess
import json
from pathlib import Path

def test_cli_email(tmp_path):
    # Create a sample email file
    email_file = tmp_path / "sample_email.txt"
    email_file.write_text("From: test@x.com\nSubject: RFQ\nBody: Please quote.")
    result = subprocess.run([
        "python", "cli.py", str(email_file)
    ], capture_output=True, text=True)
    assert "Format: Email" in result.stdout
    assert "Intent: RFQ" in result.stdout

def test_cli_json(tmp_path):
    json_file = tmp_path / "sample_invoice.json"
    json_file.write_text('{"invoice_id": "INV-1", "date": "2025-01-01", "total_amount": 100.0, "vendor": "Test", "items": ["a"]}')
    result = subprocess.run([
        "python", "cli.py", str(json_file)
    ], capture_output=True, text=True)
    assert "Format: JSON" in result.stdout
    assert "Intent: Invoice" in result.stdout

def test_cli_unknown(tmp_path):
    txt_file = tmp_path / "sample_report.txt"
    txt_file.write_text("Quarterly Report Q2 2025\nRevenue: $500,000")
    result = subprocess.run([
        "python", "cli.py", str(txt_file)
    ], capture_output=True, text=True)
    assert "Format: Text" in result.stdout
    assert "error" in result.stdout or "validation_errors" in result.stdout
