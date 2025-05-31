import json
from datetime import datetime
import uuid

# Try to import and connect to Redis, but make it optional
try:
    import redis
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.ping()
    REDIS_AVAILABLE = True
except Exception:
    r = None
    REDIS_AVAILABLE = False

def log_to_memory(data, filename="outputs/logs.json", redis_key=None, thread_id=None):
    # Generate a unique ID for this log entry
    entry_id = str(uuid.uuid4())
    # Use provided thread_id or generate a new one if not present
    if not thread_id:
        thread_id = str(uuid.uuid4())
    try:
        with open(filename, "r") as f:
            logs = json.load(f)
    except:
        logs = []

    log_entry = {
        "id": entry_id,
        "thread_id": thread_id,
        "timestamp": datetime.now().isoformat(),
        **data
    }
    logs.append(log_entry)

    with open(filename, "w") as f:
        json.dump(logs, f, indent=2)

    # Optionally log to Redis if available and requested
    if REDIS_AVAILABLE and r is not None:
        try:
            if redis_key:
                r.set(redis_key, json.dumps(log_entry))
            r.rpush(f"thread:{thread_id}", json.dumps(log_entry))
        except Exception as e:
            print(f"[Memory] Redis logging skipped: {e}")

def log_to_redis(key, data):
    if REDIS_AVAILABLE and r is not None:
        try:
            r.set(key, json.dumps(data))
        except Exception as e:
            print(f"[Memory] Redis logging skipped: {e}")

def get_from_redis(key):
    if REDIS_AVAILABLE and r is not None:
        import inspect
        import asyncio
        try:
            raw = r.get(key)
            if inspect.isawaitable(raw):
                raw = asyncio.get_event_loop().run_until_complete(raw)
            if raw:
                return json.loads(raw.decode('utf-8'))
        except Exception as e:
            print(f"[Memory] Redis get skipped: {e}")
    return None

def get_thread_history(thread_id):
    if REDIS_AVAILABLE and r is not None:
        try:
            entries = r.lrange(f"thread:{thread_id}", 0, -1)
            # If entries is awaitable, resolve it
            if hasattr(entries, '__await__'):
                import asyncio
                entries = asyncio.get_event_loop().run_until_complete(entries)
            if entries:
                return [json.loads(e.decode('utf-8')) for e in entries]
        except Exception as e:
            print(f"[Memory] Redis thread history skipped: {e}")
    return []
