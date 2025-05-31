import json
from datetime import datetime

def log_to_memory(data, filename="outputs/logs.json"):
    try:
        with open(filename, "r") as f:
            logs = json.load(f)
    except:
        logs = []

    logs.append({
        "timestamp": datetime.now().isoformat(),
        **data
    })

    with open(filename, "w") as f:
        json.dump(logs, f, indent=2)
