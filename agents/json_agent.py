import json
from pydantic import BaseModel, ValidationError, Field

class InvoiceSchema(BaseModel):
    invoice_id: str
    date: str
    total_amount: float
    vendor: str
    items: list

def process_json(content: str):
    """
    Parses JSON string, validates with InvoiceSchema, and returns structured data or errors.
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
