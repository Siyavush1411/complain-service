from sqlalchemy.orm import Session
from sqlalchemy.sql.base import _kw_reg_for_dialect
from models.complaint import Complaint
from shemas.complaint_shema import ComplaintCreate


class ComplaintRepository:
    def __init__(self, session: Session) -> None:
        self._db = session

    def create_complaint(self):
        db_complaint = Complaint(text=ComplaintCreate)
        self._db.add(db_complaint)
        self._db.commit()
        self._db.refresh(db_complaint)
        return db_complaint

    def update_complaint(self, complaint_id: int, **kwargs):
        db_complaint = (
            self._db.query(Complaint).filter(Complaint.id == complaint_id).first()
        )

        if not db_complaint:
            return None

        for key, value in kwargs.items():
            setattr(db_complaint, key, value)

        self._db.commit()
        self._db.refresh(db_complaint)
        return db_complaint
