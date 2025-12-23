import asyncio
import openai
import json
from typing import Any, Callable, List

from app.core.config import settings
from app.core.logging_config import logger
from app.models.record import Record
from app.services.interfaces.llm_service import LLMService

class OpenAILLMService(LLMService):
    def __init__(self):
        self._client = openai.OpenAI(api_key=settings.OPENAI_API_KEY, base_url=settings.OPENAI_BASE_URL)
        self._embed_model = "l2-text-embedding-3-small"
        self._chat_model = "l2-gpt-4o-mini"
        self._parse_model = "l2-gpt-4o"
        self._max_retries = 5
        self._initial_backoff = 3

    async def generate_embedding(self, text) -> List[float]:
        response = await self._with_retry(
            self._client.embeddings.create, 
            input=text, 
            model=self._embed_model)

        return response.data[0].embedding
    
    async def generate_summary(self, query: str, system_prompt: str, user_prompt: str, records: List[Record]) -> str:
        items = [record.model_dump() for record in records]
        json_data = json.dumps(items, indent=2)
        system_prompt = system_prompt.format(query=query)
        user_message = user_prompt.format(query=query, json_data=json_data)

        return await self.generate_text(
            system_prompt=system_prompt,
            user_message=user_message,
            temperature=0.2
        )

    async def generate_text(self, system_prompt: str, user_message: str, temperature: float = 0.2, max_tokens: int = 1500) -> str:
        response = await self._with_retry(
            self._client.chat.completions.create,
            model=self._chat_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    
    async def generate_object(self, system_prompt: str, user_message: str, response_format: type, temperature: float = 0.1, max_tokens: int = 500):
        response = await self._with_retry(
            self._client.chat.completions.parse,
            model=self._parse_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            response_format=response_format,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.parsed
    
    async def _with_retry(self, func: Callable[..., Any], *args, **kwargs) -> Any:
        backoff_time = self._initial_backoff
        for retry in range(self._max_retries):
            try:
                return await asyncio.to_thread(func, *args, **kwargs)
            except openai.RateLimitError:
                if retry == self._max_retries - 1:
                    logger.error(f"OpenAI Rate Limit failed after {self._max_retries} attempts")
                    raise Exception("Exceeded max retries due to rate limiting.")
                
                await asyncio.sleep(backoff_time)
                backoff_time *= 2
            except Exception as e:
                logger.error(f"Critical OpenAI failure: {str(e)}")
                raise e
    
    

