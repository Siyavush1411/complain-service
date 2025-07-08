import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    SENTIMENT_API_KEY = os.getenv("SENTIMENT_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


settings = Settings()
