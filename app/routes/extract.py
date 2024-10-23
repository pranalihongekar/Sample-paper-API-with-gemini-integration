from fastapi import APIRouter, UploadFile, File, HTTPException ,BackgroundTasks
from app.routes.gemini_utils import upload_to_gemini, wait_for_files_active, model
import json
from app.services.db import tasks_collection  # Import the tasks_collection from the db module
import asyncio
import uuid
router = APIRouter()
from pydantic import BaseModel, Field ,ValidationError, RootModel
from typing import List, Optional, Dict, Any

class QuestionParams(RootModel):
    root: Dict[str, Any] = Field(default_factory=dict)

class Question(BaseModel):
    question: str
    answer: str
    type: str
    question_slug: str
    reference_id: Optional[str] = None
    hint: Optional[str] = None
    params: QuestionParams = Field(default_factory=QuestionParams)

class Section(BaseModel):
    marks_per_question: Optional[int] = None
    type: Optional[str] = None  # Changed to Optional[str]
    questions: List[Question]

class Params(BaseModel):
    board: str
    grade: int  
    subject: str

class DocumentSchema(BaseModel):
    title: str
    type: str
    time: int
    marks: int
    params: Params
    tags: List[str]
    chapters: List[str]
    sections: List[Section]


async def process_pdf(task_id: str, temp_file_path: str):
    try:
        # ... existing code ...
        # Simulate file upload and extraction using Gemini API
        uploaded_file = upload_to_gemini(temp_file_path, mime_type="application/pdf")

        # Assume you call Gemini and get the extracted JSON
        chat_session = model.start_chat(
            history=[{"role": "user", "parts": [uploaded_file]}]
        )
        response = chat_session.send_message("Please extract the information from this document.")

        try:
            extracted_json = json.loads(response.text)
            validated_json = DocumentSchema(**extracted_json)
            print("Validation successful")
            await tasks_collection.update_one(
                {"_id": task_id},
                {"$set": {"status": "COMPLETED", "result": validated_json.model_dump()}}
            )
        except ValidationError as e:
            print(f"Validation error: {e}")
            await tasks_collection.update_one(
                {"_id": task_id},
                {"$set": {"status": "FAILED", "error": str(e)}}
            )
    except Exception as e:
        await tasks_collection.update_one(
            {"_id": task_id},
            {"$set": {"status": "FAILED", "error": str(e)}}
        )

# API to accept the PDF and start the extraction process
@router.post("/extract/pdf")
async def extract_info_from_pdf(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    try:
        temp_file_path = f"/tmp/{file.filename}"
        with open(temp_file_path, "wb") as f:
            f.write(await file.read())

        # Generate a UUID for the task_id
        task_id = str(uuid.uuid4())  # Generate unique task_id

        # Insert task into MongoDB with initial status "PROCESSING"
        await tasks_collection.insert_one({"_id": task_id, "status": "PROCESSING", "result": None})

        # Add the PDF processing to the background task queue
        background_tasks.add_task(process_pdf, task_id, temp_file_path)

        # Return the task_id immediately, without waiting for the processing to complete
        return {"task_id": task_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@router.post("/extract/text")
async def extract_info_from_text(text: str):
    try:
        chat_session = model.start_chat(history=[{"role": "user", "parts": [text]}])
        response = chat_session.send_message("Please extract the information from this text.")
        # import pdb; pdb.set_trace()
        response_dict = json.loads(response.text)
        return response_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
