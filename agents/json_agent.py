"""
JSON and Complaint Agents
- Validates and extracts fields from JSON invoices.
- Extracts complaint info from text.
"""

import json
from pydantic import BaseModel, ValidationError
from typing import Dict


class InvoiceSchema(BaseModel):
    """
    Pydantic schema for validating invoice JSON structure.
    """
    invoice_id: str
    date: str
    total_amount: float
    vendor: str
    items: list


def process_json(content: str):
    """
    Parses JSON string, validates with InvoiceSchema, and returns structured data or errors.
    Adds validation_errors if required fields are missing or invalid.

    Args:
        content (str): The JSON content as a string.

    Returns:
        dict: Extracted data and errors (if any).
    """
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print("[JSON Agent] Invalid JSON:", e)
        return {"error": str(e)}

    try:
        invoice = InvoiceSchema(**data)
        print("[JSON Agent] Valid JSON.")
        return {"data": invoice.dict(), "errors": None}
    except ValidationError as e:
        print("[JSON Agent] Validation errors:", e.errors())
        return {"data": None, "errors": e.errors()}


def process_complaint(content: str) -> Dict:
    """
    Extracts complainant, subject, and complaint body from plain text.
    Flags missing fields in validation_errors.

    Args:
        content (str): The complaint text.

    Returns:
        dict: Extracted complainant, subject, body, and raw content.
    """
    complainant = None
    subject = None
    body = None
    for line in content.splitlines():
        if line.lower().startswith("from:"):
            complainant = line.split(":", 1)[1].strip()
        elif line.lower().startswith("subject:"):
            subject = line.split(":", 1)[1].strip()
        elif line.lower().startswith("body:"):
            body = line.split(":", 1)[1].strip()
    return {
        "complainant": complainant,
        "subject": subject,
        "body": body,
        "raw_content": content[:100]
    }
