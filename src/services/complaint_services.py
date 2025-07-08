import asyncio

from fastapi.background import P

from api.openai_client import OpenAIClient
from api.sentiment_client import SentimentClient
from common.enums import ComplaintCategory, SentimentType
from config.settings import Settings
from repositories.complaint_repository import ComplaintRepository


class ComplaintAiService:
    def __init__(self, complaint_repo: ComplaintRepository):
        self.complaint_db = complaint_repo
        self.sentiment_client = SentimentClient(
            api_key=Settings.SENTIMENT_API_KEY
        )
        self.openai_client = OpenAIClient(
            api_key=Settings.OPENAI_API_KEY
        )

    async def process_complaint(self, complaint_id: int, text: str):
        sentiment = await self.sentiment_client.analyze(text)
        category = await self.openai_client.get_complaint_category(text)
        
        await self.complaint_db.update_complaint(
            complaint_id=complaint_id,
            sentiment=sentiment,
            category=category
        )