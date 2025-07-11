import telebot
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.config.settings import Settings
from src.repositories.subscriber_repository import SubscriberRepository

SQLALCHEMY_DATABASE_URL = "sqlite:///./complaints.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Session:
    db = SessionLocal()
    try:    
        yield db
    finally:
        db.close()


bot = telebot.TeleBot(Settings.TELEGRAM_BOT_TOKEN)  # type: ignore


def run_bot():
    bot.polling(none_stop=True)


@bot.message_handler(commands=["start"])
def handle_start(message):
    try:
        db = next(get_db())  # type: ignore 
        repo = SubscriberRepository(db)
        subscriber = repo.add_subscriber(message.chat.id)
        if subscriber:
            bot.reply_to(message, "Tы успешно подписан!")
        else:
            bot.reply_to(message, "Ты уже подписан.")
    finally:
        pass