from pydantic import BaseModel
from datetime import datetime


class ComplaintCreate(BaseModel):
    text: str


class ComplaintResponse(BaseModel):
    id: int
    text: str
    status: str
    timestamp: datetime
    sentiment: str
    category: str