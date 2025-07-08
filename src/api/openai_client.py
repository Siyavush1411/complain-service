import logging

from openai import OpenAI
from openai.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

from common.constants import PROMPT_FOR_GPT
from common.enums import ComplaintCategory

logger = logging.getLogger(__name__)


class OpenAIClient:
    def __init__(self, api_key: str, base_url: str = "https://openrouter.ai/api/v1"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    async def get_complaint_category(self, text: str) -> ComplaintCategory:
        messages = [
            ChatCompletionSystemMessageParam(
                role="system", content=PROMPT_FOR_GPT
            ),
            ChatCompletionUserMessageParam(role="user", content=f'Жалоба: "{text}"'),
        ]

        logger.debug("Отправка запроса в OpenAI...")
        logger.debug("Model: openai/gpt-4o")
        logger.debug("Messages: %s", messages)

        try:
            response = self.client.chat.completions.create(
                model="openai/gpt-4o", messages=messages, temperature=0.0, max_tokens=10
            )

            logger.debug("Ответ от OpenAI получен: %s", response)

            category_raw = response.choices[0].message.content.strip().lower()
            logger.debug("Распознанная категория: %s", category_raw)

            if category_raw in ["техническая", "оплата"]:
                return ComplaintCategory(category_raw)
            return ComplaintCategory.OTHER

        except Exception as e:
            logger.exception("💥 Ошибка при вызове OpenAI: %s", str(e))
            return ComplaintCategory.OTHER
