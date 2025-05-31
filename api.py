from agents.classifier_agent import classify_input

def classify_file(file):
    content = file.read()
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        text = "[Binary Content]"

    format_, intent = classify_input(text, file.filename)

    return {
        "filename": file.filename,
        "format": format_,
        "intent": intent,
        "content_sample": text[:100]
    }
