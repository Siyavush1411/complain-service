from datetime import timedelta, datetime
from common.enums import ComplaintCategory
from sqlalchemy.orm import Session
from models.complaint import Complaint
from schemas.complaint_schema import ComplaintCreate


class ComplaintRepository:
    def __init__(self, session: Session = Session()) -> None:
        self._db = session

    async def create_complaint(self, complaint: ComplaintCreate) -> Complaint: 
        db_complaint = Complaint(text=complaint.text) 
        self._db.add(db_complaint)
        self._db.commit()
        self._db.refresh(db_complaint)
        return db_complaint

    async def update_complaint(
        self, complaint_id: int, **kwargs
    ) -> Complaint | None:
        db_complaint = (
            self._db.query(Complaint)
            .filter(Complaint.id == complaint_id)
            .first()
        )

        if not db_complaint:
            return None     
        for key, value in kwargs.items():
            setattr(db_complaint, key, value)

        self._db.commit()
        self._db.refresh(db_complaint)   
        return db_complaint
    
    # ну по дефолту за последний час будет собирать открытые жалобы
    async def get_open_complaint(self, hours: int = 1):
        time_threshold = datetime.utcnow() - timedelta(hours=hours)
        return self._db.query(Complaint).filter(
            Complaint.status == "open",
            Complaint.timestamp >= time_threshold
        ).all()
        
    async def get_open_technical_complaint(self, hours: int = 1):
        time_threshold = datetime.utcnow() - timedelta(hours=hours)
        return self._db.query(Complaint).filter(
            Complaint.status == "open",
            Complaint.timestamp >= time_threshold,
            Complaint.category == ComplaintCategory.TECHNICAL
        ).all()