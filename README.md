# Multi-Agent AI Router

## 🧠 Project Summary
A Python-based AI system that reads documents or messages (PDFs, JSON files, or emails), understands their content and intent, and routes them to specialized agents for automated processing.

---

## 🔍 Goal
Automate the classification and processing of various business documents (invoices, product requests, complaints, etc.) to reduce manual effort and errors.

---

## 🧩 How It Works
1. **Input:** Send a file (PDF, Email, or JSON) to the system.
2. **Classification:** The Classifier Agent determines the file type and intent (e.g., "Invoice", "Complaint", "RFQ").
3. **Routing:** The input is routed to the appropriate agent:
   - **Email Agent:** Extracts sender, topic, urgency, and structures the data.
   - **JSON Agent:** Validates and cleans up JSON, flags issues.
   - **(PDF Agent):** (To be implemented) Handles PDF extraction.
4. **Memory Store:** All extracted information is logged in a shared memory module for traceability and chaining.

---

## 🚦 What This System Can Do

- Automatically classify documents as Email, JSON, PDF, or Text.
- Detect the intent of a document: RFQ (Request for Quote), Invoice, Complaint, Purchase Order, Support Ticket, and more.
- Route each document to the correct specialized agent for extraction:
  - Email Agent: Extracts sender, urgency, and content from emails.
  - JSON Agent: Validates and extracts fields from structured JSON invoices.
  - Complaint Agent: Extracts complainant, subject, and body from complaints (PDF or text).
- Log all results to outputs/logs.json with timestamp, format, intent, and extracted data.
- (Optional) Log to Redis for advanced memory, chaining, and thread tracking.
- CLI interface for easy batch or single-file processing.
- Easily extensible: add new agents, intents, or formats as needed.

---

## 🧠 Agents in the System
- **Classifier Agent (`agents/classifier_agent.py`):**
  - Entry point. Detects file format and intent using Hugging Face transformers (zero-shot-classification) or fallback keyword logic.
  - Routes to the correct agent and returns results.
- **Email Agent (`agents/email_agent.py`):**
  - Parses emails, extracts sender, topic, urgency, and structures the data.
- **JSON Agent (`agents/json_agent.py`):**
  - Handles structured data, validates, cleans, and flags anomalies.
- **Shared Memory Module (`memory/memory_store.py`):**
  - Central logbook for all agents, storing sender, file type, intent, extracted fields, timestamps, and unique IDs.
  - Supports both file-based (outputs/logs.json) and Redis-based logging.

---

## 📂 File-by-File Overview

- **main.py**
  - Runs a hardcoded example (sample_email.txt), classifies and processes it, and logs the result to outputs/logs.json.
- **cli.py**
  - Command-line interface. You specify a file, it classifies, routes, prints, and logs the result.
- **api.py**
  - (Currently unused, but can be used for a FastAPI web interface if needed.)
- **agents/classifier_agent.py**
  - Detects file type and intent, routes to the correct agent, and returns results.
- **agents/email_agent.py**
  - Extracts sender, urgency, and raw content from emails.
- **agents/json_agent.py**
  - (Stub) Validates and extracts fields from JSON files.
- **memory/memory_store.py**
  - Handles logging to outputs/logs.json and optionally to Redis.
- **outputs/logs.json**
  - Stores all processed and extracted results as a list of JSON objects.
- **data/sample_email.txt**
  - Example input file for testing the pipeline.

---

## 🔄 Example Workflow

Suppose you run:
```sh
python cli.py data/sample_email.txt
```

### What Happens:
1. **cli.py** parses the argument and calls `classify_and_route` from `agents/classifier_agent.py`.
2. **classifier_agent.py** reads the file, detects format (Email) and intent (RFQ), and routes to the Email Agent.
3. **email_agent.py** extracts:
   - sender: client@abc.com
   - urgency: Normal
   - raw_content: The first 100 characters of the email.
4. The CLI prints:
   - Format: Email
   - Intent: RFQ
   - Agent Result: The extracted info as a dictionary.
5. The result is logged to `outputs/logs.json`:
```json
[
  {
    "timestamp": "2025-05-31T21:13:57.332559",
    "source": "data/sample_email.txt",
    "format": "Email",
    "intent": "RFQ",
    "extracted": {
      "sender": "client@abc.com",
      "urgency": "Normal",
      "raw_content": "From: client@abc.com\nSubject: Request for Quote\nBody: Please send a quote for 50 units.\n"
    }
  }
]
```

---

## 💻 Technologies Used
- **Python** – Main language
- **Hugging Face Transformers** – For text understanding and classification
- **Redis** – For optional shared memory storage
- **Email/PDF parsers** – For input processing
- **CLI** – For running/testing

---

## 🚀 Setup Instructions

### 1. Create a Virtual Environment
On macOS and Linux:
```sh
python3 -m venv venv
```
On Windows:
```sh
python -m venv venv
```
> **Note:** If you see `zsh: command not found: python`, use `python3` instead of `python`.

### 2. Activate the Virtual Environment
On macOS/Linux:
```sh
source venv/bin/activate
```
On Windows:
```sh
venv\Scripts\activate
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Run the Main Script or CLI
```sh
python main.py
# or, for custom files:
python cli.py data/sample_email.txt
```

This will process the sample email and log the output to `outputs/logs.json`.

---

## 📑 Example Input (data/sample_email.txt)
```
From: client@abc.com
Subject: Request for Quote
Body: Please send a quote for 50 units.
```

---

## 📦 Project Structure
```
ai_agent/
├── agents/
│   ├── classifier_agent.py
│   ├── email_agent.py
│   └── json_agent.py
├── cli.py
├── main.py
├── api.py
├── memory/
│   └── memory_store.py
├── data/
│   ├── sample_email.txt
│   ├── sample_invoice.json
│   └── sample_complaint.pdf
├── outputs/
│   └── logs.json
├── requirements.txt
├── README.md
└── ...
```

---

## 🛠️ Development Notes
- Update README.md for any new features or changes.
- Use .gitignore to avoid committing venv/, __pycache__/, and outputs/.
- If you want a web interface, restore FastAPI code in api.py and run with uvicorn.
- For Redis logging, ensure Redis server is running locally.

---

## 📝 Changelog
- CLI now logs all results to outputs/logs.json.
- Classifier agent uses Hugging Face transformers for intent detection.
- All major files and their roles are documented above.

---

## 📚 References
- [Hugging Face Transformers Documentation](https://huggingface.co/docs/transformers/index)
- [Python argparse Documentation](https://docs.python.org/3/library/argparse.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

## ❓ Questions & Support
If you have questions or want to extend the system, see the comments in each file and the step-by-step project log in `text` for rationale and build history.

---

## 🧠 Logging & Memory Features
- Each log entry includes a unique id and a thread_id for tracking and chaining related document processing sessions.
- All logs are stored in outputs/logs.json for traceability.
- If Redis is available, logs are also stored in Redis, enabling advanced memory, chaining, and thread-based history.
- The CLI supports a --thread-id argument to group related logs together.
- The system is robust: if Redis is not running, file-based logging always works and the system never crashes.

---
