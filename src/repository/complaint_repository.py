from sqlalchemy.orm import Session
from models.complaint import Complaint
from shemas.complaint_shema import ComplaintCreate, ComplaintResponse


class ComplaintRepository:
    def __init__(self, session: Session) -> None:
        self._db = session

    def create_complian(self):
        db_complaint = Complaint(text=ComplaintCreate)
        self._db.add(db_complaint)
        self._db.commit()
        self._db.refresh(db_complaint)
        return db_complaint
