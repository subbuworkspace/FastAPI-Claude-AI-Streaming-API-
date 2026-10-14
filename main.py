
"""
FastAPI + Claude AI Streaming API
Author: Subrata Mondal

Features:
- REST API endpoints
- Pydantic request validation
- Patient CRUD operations
- JSON file storage
- Claude AI streaming using SSE
- Environment variable configuration
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

# Load environment variables from .env
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

DATA_FILE = BASE_DIR / "patients.json"

app = FastAPI(
    title="FastAPI + Claude AI",
    description="REST API, CRUD operations, and Claude AI streaming",
    version="1.0.0",
)

# Optional Claude integration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.getenv(
    "ANTHROPIC_MODEL",
    "claude-sonnet-4-20250514",
)

claude_client = None

if ANTHROPIC_API_KEY:
    try:
        from anthropic import Anthropic
        claude_client = Anthropic(api_key=ANTHROPIC_API_KEY)
    except ImportError:
        pass


# -------------------- Pydantic Models --------------------

class Patient(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0, le=120)
    condition: str = Field(min_length=1, max_length=150)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10000)
    max_tokens: int = Field(default=200, ge=1, le=4096)


# -------------------- JSON Helper Functions --------------------

def load_patients():
    """Read patient records from patients.json."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="patients.json file not found",
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Invalid JSON format in patients.json",
        )

    if not isinstance(data, list):
        raise HTTPException(
            status_code=500,
            detail="patients.json must contain a JSON list",
        )

    return data


def save_patients(patients):
    """Save patient records to patients.json."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(patients, file, indent=2, ensure_ascii=False)


# -------------------- General Endpoints --------------------

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Welcome to the FastAPI + Claude AI project!",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# -------------------- Patient CRUD Endpoints --------------------

@app.get("/patients", response_model=list[Patient])
def get_all_patients():
    """Retrieve all patient records."""
    return load_patients()


@app.get("/patients/{patient_id}", response_model=Patient)
def get_patient(patient_id: int):
    """Retrieve one patient by ID."""
    for patient in load_patients():
        if patient["id"] == patient_id:
            return patient

    raise HTTPException(
        status_code=404,
        detail="Patient not found",
    )


@app.post(
    "/patients",
    response_model=Patient,
    status_code=status.HTTP_201_CREATED,
)
def create_patient(patient: Patient):
    """Create a patient record."""
    patients = load_patients()

    if any(item["id"] == patient.id for item in patients):
        raise HTTPException(
            status_code=409,
            detail="Patient ID already exists",
        )

    patients.append(patient.model_dump())
    save_patients(patients)

    return patient


@app.put("/patients/{patient_id}", response_model=Patient)
def update_patient(patient_id: int, updated_patient: Patient):
    """Replace an existing patient record."""
    if updated_patient.id != patient_id:
        raise HTTPException(
            status_code=400,
            detail="Path ID must match the patient ID in the body",
        )

    patients = load_patients()

    for index, patient in enumerate(patients):
        if patient["id"] == patient_id:
            patients[index] = updated_patient.model_dump()
            save_patients(patients)
            return patients[index]

    raise HTTPException(
        status_code=404,
        detail="Patient not found",
    )


@app.delete(
    "/patients/{patient_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_patient(patient_id: int):
    """Delete a patient record."""
    patients = load_patients()
    remaining = [
        patient for patient in patients
        if patient["id"] != patient_id
    ]

    if len(remaining) == len(patients):
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        )

    save_patients(remaining)


# -------------------- Claude AI Streaming --------------------

@app.post("/chatbot/stream")
def chat_stream(request: ChatRequest):
    """Stream Claude AI responses as Server-Sent Events."""
    if not ANTHROPIC_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="Configure ANTHROPIC_API_KEY in your .env file",
        )

    if claude_client is None:
        raise HTTPException(
            status_code=500,
            detail="Anthropic SDK unavailable. Install requirements.txt",
        )

    def generate():
        try:
            with claude_client.messages.stream(
                model=ANTHROPIC_MODEL,
                max_tokens=request.max_tokens,
                messages=[
                    {
                        "role": "user",
                        "content": request.message,
                    }
                ],
            ) as stream:
                for text_chunk in stream.text_stream:
                    # JSON encoding safely handles special characters.
                    event_data = json.dumps({"text": text_chunk})
                    yield f"data: {event_data}\n\n"

            yield f"data: {json.dumps({'done': True})}\n\n"

        except Exception:
            # Do not expose API keys or raw provider errors.
            error_data = json.dumps(
                {"error": "Claude request failed. Check server logs and model access."}
            )
            yield f"event: error\ndata: {error_data}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
