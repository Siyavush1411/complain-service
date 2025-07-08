import requests
from openai import OpenAI

from config.settings import Settings
from repository.complaint_repository import ComplaintRepository


class ComplaintAiService():
    def __init__(self, complaint_repo: ComplaintRepository):
        self.complaint_db = complaint_repo
        self.client = OpenAI(api_key=Settings.OPENAI_API_KEY) 
           
    def analyze_sentiment(self, text: str):
        try:
            response = requests.post(
                "https://api.apilayer.com/sentiment/analysis",
                headers={"apikey": Settings.SENTIMENT_API_KEY},
                data=text.encode("utf-8")
            )
            response.raise_for_status()
            return response.json().get("sentiment", {}).get("type", "unknown")
        except Exception:
            return "unknown"


    def determine_category(self, text: str) -> str:
        messages = [
            {
                "role": "system",
                "content": "Определи категорию жалобы. Варианты: техническая, оплата, другое. Ответ только одним словом."
            },
            {
                "role": "user",
                "content": f'Жалоба: "{text}"'
            }
        ]
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.0,
                max_tokens=10
            )
            category = response.choices[0].message.content.strip().lower()
            return category if category in ["техническая", "оплата"] else "другое"
        except Exception:
            return "другое"

    def process_complaint(self, complaint_id: int, text: str):
        sentiment = self.analyze_sentiment(text)
        category = self.determine_category(text)
        
        self.complaint_db.update_complaint(
            complaint_id=complaint_id,
            sentiment=sentiment,
            category=category
        )        )