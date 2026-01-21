from typing import List

from app.core.config import settings
from app.core.prompts import PARSE_SYSTEM_PROMPT, PARSE_USER_MESSAGE, CONDENSE_SYSTEM_PROMPT, CONDENSE_USER_MESSAGE
from app.models.intent_context import IntentContext
from app.services.interfaces.llm_service import LLMService
from app.services.interfaces.nlp_processor import NLPProcessor

class LLMNLPProcessor(NLPProcessor):
    def __init__(self, llm_service: LLMService):
        self._llm_service = llm_service

    async def process_query(self, query: str) -> IntentContext:
        user_message = PARSE_USER_MESSAGE.format(query=query)
        
        return await self._llm_service.generate_object(
                system_prompt=PARSE_SYSTEM_PROMPT,
                user_message=user_message,
                response_format=IntentContext
            )
        
    async def condense_query(self, history: List[str]) -> str:
        if not history:
            return ""
        
        user_message = CONDENSE_USER_MESSAGE.format(history="\n".join(history))
        return await self._llm_service.generate_text(
            system_prompt=CONDENSE_SYSTEM_PROMPT,
            user_message=user_message,
            model=settings.OPENAI_CONDENSE_MODEL,
            temperature=settings.OPENAI_CONDENSE_TEMPERATURE,
            max_tokens=settings.OPENAI_CONDENSE_MAX_TOKENS,
            top_p=settings.OPENAI_CONDENSE_TOP_P
        )