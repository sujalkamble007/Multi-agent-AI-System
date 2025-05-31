import json

def process_json(content: str):
    """
    Simple JSON Agent stub.
    Parses JSON string and flags missing fields.
    """
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print("[JSON Agent] Invalid JSON:", e)
        return None

    required_fields = ["invoice_id", "date", "total_amount"]
    missing_fields = [f for f in required_fields if f not in data]

    if missing_fields:
        print(f"[JSON Agent] Missing fields: {missing_fields}")
    else:
        print("[JSON Agent] All required fields present.")

    # Return parsed data and missing fields info
    return {
        "data": data,
        "missing_fields": missing_fields
    }
