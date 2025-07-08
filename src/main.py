from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import asyncio

# Импорты из новой структуры
from repository.session import get_db
from schemas.complaint_schema import ComplaintCreate, ComplaintResponse
from repository.complaint_repository import ComplaintRepository
from services.complaint_tone import ComplaintAiService

app = FastAPI(
    title="Complaint Handling System API",
    description="API for processing customer complaints with AI analysis",
    version="1.0.0",
)

@app.post(
    "/complaints/",
    response_model=ComplaintResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new complaint",
    response_description="The created complaint with initial status",
)
async def create_complaint(
    complaint: ComplaintCreate, 
    db: Session = Depends(get_db)
):
    """
    Create a new customer complaint with:
    - **text**: Complaint content (required)
    - AI will automatically analyze sentiment and category (async)
    """
    complaint_repo = ComplaintRepository(session=db)
    ai_service = ComplaintAiService(complaint_repo)
    
    db_complaint = complaint_repo.create_complaint(complaint)
    
    asyncio.create_task(
        ai_service.process_complaint(
            complaint_id=db_complaint.id,
            text=complaint.text
        )
    )
    
    return db_complaint

@app.get(
    "/complaints/open/",
    summary="Get recent open complaints",
    description="Returns complaints with status=open from the last N hours"
)
def get_recent_open_complaints(
    hours: int = 1,
    db: Session = Depends(get_db)
):
    complaint_repo = ComplaintRepository(session=db)
    return complaint_repo.get_open_complaint(hours=hours)

@app.patch(
    "/complaints/{complaint_id}/close/",
    status_code=status.HTTP_200_OK,
    summary="Close a complaint",
    responses={
        404: {"description": "Complaint not found"},
        200: {"description": "Successfully closed"}
    }
)
def close_complaint(
    complaint_id: int, 
    db: Session = Depends(get_db)
):
    """
    Close a complaint by ID:
    - Updates status to 'closed'
    - Returns success message
    """
    complaint_repo = ComplaintRepository(session=db)
    db_complaint = complaint_repo.update_complaint(
        complaint_id=complaint_id,
        status="closed"
    )
    
    if not db_complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found"
        )
    
    return {"status": "success", "message": "Complaint closed"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)