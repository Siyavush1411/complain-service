import logging

import httpx
from openai import OpenAI
from openai.types.chat import (ChatCompletionSystemMessageParam,
                               ChatCompletionUserMessageParam)

from config.settings import Settings
from repository.complaint_repository import ComplaintRepository


class ComplaintAiService():
    def __init__(self, complaint_repo: ComplaintRepository):
        self.complaint_db = complaint_repo
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=Settings.OPENAI_API_KEY
        )
           
    async def analyze_sentiment(self, text: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.apilayer.com/sentiment/analysis",
                    headers={"apikey": str(Settings.SENTIMENT_API_KEY)},
                    data={"text": text}
                )
                response.raise_for_status()
                return await (
                    response.json()
                    .get("sentiment", {})
                    .get("type", "unknown")
                )
        except Exception:
            return "unknown"


    async def determine_category(self, text: str) -> str:
        messages = [
            ChatCompletionSystemMessageParam(
                role="system",
                content="Определи категорию жалобы. Варианты: техническая, оплата, другое. Ответ только одним словом."
            ),
            ChatCompletionUserMessageParam(
                role="user",
                content=f'Жалоба: "{text}"'
            )
        ]
        try:
            response = self.client.chat.completions.create(
                model="openai/gpt-4o",
                messages=messages,
                temperature=0.0,
                max_tokens=10
            )

            category = response.choices[0].message.content.strip().lower()
            return category if category in ["техническая", "оплата"] else "другое"
        except Exception as e:
            logging.error("Ошибка при вызове OpenAI: %s", str(e))
            return "другое"

    async def process_complaint(self, complaint_id: int, text: str):
        sentiment = await self.analyze_sentiment(text)
        category = await self.determine_category(text)
        
        await self.complaint_db.update_complaint(
            complaint_id=complaint_id,
            sentiment=sentiment,
            category=category
        )