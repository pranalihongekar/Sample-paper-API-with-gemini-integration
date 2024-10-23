from fastapi import APIRouter, HTTPException
from app.services.db import tasks_collection
from bson import ObjectId

router = APIRouter()

@router.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    # No need to convert to ObjectId, use it as a string
    task = await tasks_collection.find_one({"_id": task_id})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"task_status": task.get("status", "Unknown")}

@router.get("/tasks/{task_id}/result")
async def get_extracted_result(task_id: str):
    task = await tasks_collection.find_one({"_id": task_id})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.get("status") != "COMPLETED":
        raise HTTPException(status_code=400, detail="Task not yet completed")

    return task.get("result", {})
