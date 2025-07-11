from sqlalchemy.orm import Session

from src.core.models.subscriber import Subscriber


class SubscriberRepository:
    def __init__(self, session: Session):
        self._db = session

    def get_subscriber_by_user_id(self, user_id: int) -> Subscriber | None:
        return (
            self._db.query(Subscriber)
            .filter(Subscriber.user_id == user_id)
            .first()
        )
        
    def add_subscriber(self, user_id: int) -> Subscriber:
        new_subscriber = Subscriber(chat_id=user_id)
        self._db.add(new_subscriber)
        self._db.commit()
        self._db.refresh(new_subscriber)
        return new_subscriber

    def get_all_subscribers(self) -> list[Subscriber]:
        return self._db.query(Subscriber).all()
