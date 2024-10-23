from fastapi import APIRouter, HTTPException
from app.models import SamplePaper
from app.services.db import papers_collection
from app.services.redis_cache import get_cached_paper, set_cached_paper, redis_client
from bson import ObjectId

router = APIRouter()

@router.post("/papers")
async def create_paper(paper: SamplePaper):
    result = await papers_collection.insert_one(paper.dict())
    return {"paper_id": str(result.inserted_id)}

@router.get("/papers/{paper_id}")
async def get_paper(paper_id: str):
    cached_paper = get_cached_paper(paper_id)
    if cached_paper:
        return cached_paper
    
    paper = await papers_collection.find_one({"_id": ObjectId(paper_id)})
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    paper['_id'] = str(paper['_id'])#here we have to convert to string else it will throw error
    set_cached_paper(paper_id, paper)
    return paper

@router.put("/papers/{paper_id}")
async def update_paper(paper_id: str, paper_update: dict):
    update_result = await papers_collection.update_one(
        {"_id": ObjectId(paper_id)},
        {"$set": paper_update}
    )
    
    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Paper not found or no update made")

    # Invalidate Redis cache
    redis_client.delete(paper_id)

    return {"message": "Paper updated successfully"}


@router.delete("/papers/{paper_id}")
async def delete_paper(paper_id: str):
    # Delete the paper from the database
    delete_result = await papers_collection.delete_one({"_id": ObjectId(paper_id)})
    
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    # Invalidate Redis cache
    redis_client.delete(paper_id)
    
    return {"message": "Paper deleted successfully"}
