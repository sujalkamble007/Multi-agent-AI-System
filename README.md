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

## 🧠 Agents in the System
- **Classifier Agent:** Entry point. Detects file format and intent, routes to the correct agent, and logs results.
- **Email Agent:** Parses emails, extracts sender, topic, urgency, and structures the data.
- **JSON Agent:** Handles structured data, validates, cleans, and flags anomalies.
- **Shared Memory Module:** Central logbook for all agents, storing sender, file type, intent, extracted fields, timestamps, and unique IDs.

---

## 🔄 Example Workflow
1. User sends an email: "Please send a quote for 100 units of Item X"
2. **Classifier Agent:**
   - Detects format: Email
   - Intent: RFQ (Request for Quote)
   - Routes to Email Agent
3. **Email Agent:**
   - Extracts sender, intent, urgency, and structures the data
4. **Shared Memory:**
   - Stores format, intent, extracted values, timestamp, and ID

---

## 💻 Technologies Used
- **Python** – Main language
- **LLMs (OpenAI GPT, etc.)** – For text understanding and classification
- **Redis or SQLite** – For shared memory storage
- **Email/PDF parsers** – For input processing
- **Optional:** FastAPI or CLI for running/testing

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

### 4. Run the Main Script
```sh
python main.py
```

This will process the sample email and log the output to `outputs/logs.json`.
