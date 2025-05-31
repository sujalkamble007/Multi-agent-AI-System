from agents.classifier_agent import classify_input
from agents.email_agent import process_email
from memory.memory_store import log_to_memory

with open("data/sample_email.txt", "r") as f:
    content = f.read()

filename = "sample_email.txt"
format_, intent = classify_input(content, filename)

if format_ == "Email":
    extracted = process_email(content)
else:
    extracted = {"message": "Format handler not implemented yet"}

log_to_memory({
    "source": filename,
    "format": format_,
    "intent": intent,
    "extracted": extracted
})

print("✅ Processed and logged.")
