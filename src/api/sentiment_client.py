import httpx
from common.enums import SentimentType


class SentimentClient:
    def __init__(self, api_key: str):
        self.api_url = "https://api.apilayer.com/sentiment/analysis"
        self.headers = {"apikey": api_key}

    async def analyze(self, text: str) -> SentimentType:
        try:
            async with httpx.AsyncClient(timeout=3) as client:
                response = await client.post(
                    self.api_url,
                    headers=self.headers,
                    content=text.encode("utf-8")
                )

            if response.status_code != 200:
                return SentimentType.UNKNOWN

            data = response.json()
            sentiment = data.get("sentiment", "unknown").lower()
            return SentimentType(sentiment)
        except Exception:
            return SentimentType.UNKNOWN
