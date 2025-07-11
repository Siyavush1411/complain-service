import asyncio

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.services.complaint_services import ComplaintAiService
from src.repositories.complaint_repository import ComplaintRepository
from src.repositories.session import get_db
from src.repositories.subscriber_repository import SubscriberRepository
from src.schemas.complaint_schema import ComplaintCreate, ComplaintResponse

router = APIRouter()


@router.post(
    "/complaints/",
    response_model=ComplaintResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new complaint",
    response_description="The created complaint with initial status",
)
async def create_complaint(
    complaint: ComplaintCreate, db: Session = Depends(get_db)
):
    complaint_repo = ComplaintRepository(session=db)
    ai_service = ComplaintAiService(complaint_repo)

    db_complaint = await complaint_repo.create_complaint(complaint)

    asyncio.create_task(
        ai_service.process_complaint(
            complaint_id=db_complaint.id, text=complaint.text  # type: ignore
        )
    )

    return db_complaint


@router.get(
    "/complaints/open/",
    summary="Get recent open complaints",
    description="Returns complaints with status=open from the last N hours",
)
async def get_recent_open_complaints(
    hours: int = 1, db: Session = Depends(get_db)
):
    complaint_repo = ComplaintRepository(session=db)
    return await complaint_repo.get_open_complaint(hours=hours)


@router.patch(
    "/complaints/{complaint_id}/close/",
    status_code=status.HTTP_200_OK,
    summary="Close a complaint",
    responses={
        404: {"description": "Complaint not found"},
        200: {"description": "Successfully closed"},
    },
)
async def close_complaint(complaint_id: int, db: Session = Depends(get_db)):
    complaint_repo = ComplaintRepository(session=db)
    db_complaint = await complaint_repo.update_complaint(
        complaint_id=complaint_id, status="closed"
    )

    if not db_complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found"
        )

    return {"status": "success", "message": "Complaint closed"}


@router.get(
    "/all-telegram-bot-subscribers",
    summary="returned all subscribers"
)
def get_all_subscriber(db: Session = Depends(get_db)):
    subscriber_repo = SubscriberRepository(db)
    return subscriber_repo.get_all_subscribers()
