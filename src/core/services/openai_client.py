import logging

from openai import OpenAI
from openai.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

from src.core.common.constants import (
    PROMPT_FOR_CATEGORY,
    PROMPT_FOR_SENTIMENTS,
)
from src.core.common.enums import (
    ComplaintCategory,
    SentimentType,
)

logger = logging.getLogger(__name__)


class OpenAIClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://openrouter.ai/api/v1"
    ):
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    async def get_complaint_category(self, text: str) -> ComplaintCategory:
        messages = [
            ChatCompletionSystemMessageParam(
                role="system",
                content=PROMPT_FOR_CATEGORY
            ),
            ChatCompletionUserMessageParam(
                role="user",
                content=f'Жалоба: "{text}"'
            ),
        ]

        try:
            response = self.client.chat.completions.create(
                model="openai/gpt-4o",
                messages=messages,
                max_tokens=10
            )

            category_raw = (
                response.choices[0].
                message.content
                .strip().lower()  # type: ignore
            )
            logger.debug("Распознанная категория: %s", category_raw)

            if category_raw in ["техническая", "оплата"]:
                return ComplaintCategory(category_raw)
            return ComplaintCategory.OTHER

        except Exception as e:
            logger.exception("Ошиeка при вызове OpenAI: %s", str(e))
            return ComplaintCategory.OTHER

    async def get_complaint_sentiment(self, text: str) -> ComplaintCategory:
        messages = [
            ChatCompletionSystemMessageParam(
                role="system",
                content=PROMPT_FOR_SENTIMENTS
                ),
            ChatCompletionUserMessageParam(
                role="user",
                content=f'Жалоба: "{text}"'
                ),
        ]

        try:
            response = self.client.chat.completions.create(
                model="openai/gpt-4o",
                messages=messages,
                max_tokens=10
            )

            sentimet_raw = (
                response.choices[0]
                .message.content
                .strip().lower()  # type: ignore
            )
            
            logger.debug("Распознанный тон: %s", sentimet_raw)

            if sentimet_raw in ["positive", "negative", "neutral"]:
                return SentimentType(sentimet_raw)
            return SentimentType.UNKNOWN
        
        except Exception as e:
            logger.exception("Ошибка при вызове OpenAI: %s", str(e))
            return SentimentType.UNKNOWN
