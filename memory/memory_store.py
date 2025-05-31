import json
from datetime import datetime
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

def log_to_memory(data, filename="outputs/logs.json", redis_key=None):
    # Log to file as before
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

    # Optionally log to Redis if redis_key is provided
    if redis_key:
        r.set(redis_key, json.dumps(logs[-1]))

def log_to_redis(key, data):
    r.set(key, json.dumps(data))

def get_from_redis(key):
    import inspect
    import asyncio
    raw = r.get(key)
    if inspect.isawaitable(raw):
        raw = asyncio.get_event_loop().run_until_complete(raw)
    if raw:
        return json.loads(raw.decode('utf-8'))
    return None
