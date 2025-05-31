from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse, HTMLResponse
from agents.classifier_agent import classify_and_route
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import shutil
import os

app = FastAPI(title="Multi-Agent AI Router API", description="Upload a business document (Email, Invoice, Complaint, PDF, or Text) and get structured extraction results.", version="1.0.0")

# Allow CORS for local testing and web UIs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Mount static and template directories
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.post("/classify-file/", summary="Classify and extract from a business document", response_description="Classification and extraction result")
async def classify_file(file: UploadFile = File(..., description="Upload your document (txt, json, pdf, etc.)"), thread_id: str = Form(None)):
    filename = file.filename or "uploaded_file"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    format_, intent, result = classify_and_route(file_path)
    os.remove(file_path)
    # Custom output for Email: show sender and urgency directly
    if format_ == "Email":
        response = {
            "format": format_,
            "intent": intent,
            "sender": result.get("sender"),
            "urgency": result.get("urgency"),
            "raw_content": result.get("raw_content")
        }
    else:
        response = {
            "format": format_,
            "intent": intent,
            "extracted": result  # Always show the full result dict
        }
    return JSONResponse(response)

@app.get("/", include_in_schema=False)
def root():
    return {"message": "Welcome to the Multi-Agent AI Router API! Use /docs for the interactive UI."}

@app.get("/ui", include_in_schema=False)
def custom_ui(request: Request):
    return templates.TemplateResponse("ui.html", {"request": request})

# Custom OpenAPI schema for a more user-friendly UI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://cdn-icons-png.flaticon.com/512/3062/3062634.png",
        "altText": "AI Router Logo"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
