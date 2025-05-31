from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from agents.classifier_agent import classify_and_route
import shutil
import os

app = FastAPI(title="Multi-Agent AI Router API")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/classify-file/")
async def classify_file(file: UploadFile = File(...), thread_id: str = Form(None)):
    # Ensure filename is not None
    filename = file.filename or "uploaded_file"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # Classify and route
    format_, intent, result = classify_and_route(file_path)
    # Optionally, clean up uploaded file
    os.remove(file_path)
    return JSONResponse({
        "filename": filename,
        "format": format_,
        "intent": intent,
        "result": result
    })

@app.get("/")
def root():
    return {"message": "Welcome to the Multi-Agent AI Router API! Use /docs for the interactive UI."}
