import asyncio
import openai
from typing import Any, Callable, List, Optional

from app.core.config import settings
from app.core.logging_config import logger
from app.services.interfaces.llm_service import LLMService

class OpenAILLMService(LLMService):
    def __init__(self):
        self._client = openai.OpenAI(api_key=settings.OPENAI_API_KEY, base_url=settings.OPENAI_BASE_URL)

        self._embed_model = settings.OPENAI_EMBED_MODEL
        self._chat_model = settings.OPENAI_CHAT_MODEL
        self._parse_model = settings.OPENAI_PARSE_MODEL

        self._chat_temperature = settings.OPENAI_CHAT_TEMPERATURE
        self._parse_temperature = settings.OPENAI_PARSE_TEMPERATURE

        self._chat_max_tokens = settings.OPENAI_CHAT_MAX_TOKENS
        self._parse_max_tokens = settings.OPENAI_PARSE_MAX_TOKENS

        self._chat_top_p = settings.OPENAI_CHAT_TOP_P
        self._parse_top_p = settings.OPENAI_PARSE_TOP_P

        self._max_retries = settings.OPENAI_MAX_RETRIES
        self._retry_initial_backoff_seconds = settings.OPENAI_RETRY_INITIAL_BACKOFF_SECONDS
        self._retry_backoff_multiplier = settings.OPENAI_RETRY_BACKOFF_MULTIPLIER

    async def generate_embedding(
            self, 
            text, 
            model: Optional[str] = None
        ) -> List[float]:    
        response = await self._with_retry(
            self._client.embeddings.create, 
            input=text, 
            model=self._param_or_default(model, self._embed_model))

        return response.data[0].embedding
    
    async def generate_text(
            self, 
            system_prompt: str, 
            user_message: str, 
            model: Optional[str] = None, 
            temperature: Optional[float] = None, 
            max_tokens: Optional[int] = None, 
            top_p: Optional[float] = None
        ) -> str:
        response = await self._with_retry(
            self._client.chat.completions.create,
            model=self._param_or_default(model, self._chat_model),
            temperature=self._param_or_default(temperature, self._chat_temperature),
            max_tokens=self._param_or_default(max_tokens, self._chat_max_tokens),
            top_p=self._param_or_default(top_p, self._chat_top_p),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message.content
    
    async def generate_object(
            self, 
            system_prompt: str, 
            user_message: str, 
            response_format: type, 
            model: Optional[str] = None, 
            temperature: Optional[float] = None, 
            max_tokens: Optional[int] = None, 
            top_p: Optional[float] = None
        ):
        response = await self._with_retry(
            self._client.chat.completions.parse,
            model=self._param_or_default(model, self._parse_model),
            temperature=self._param_or_default(temperature, self._parse_temperature),
            max_tokens=self._param_or_default(max_tokens, self._parse_max_tokens),
            top_p=self._param_or_default(top_p, self._parse_top_p),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            response_format=response_format
        )
        return response.choices[0].message.parsed
    
    async def _with_retry(self, func: Callable[..., Any], *args, **kwargs) -> Any:
        backoff_time = self._retry_initial_backoff_seconds
        for retry in range(self._max_retries):
            try:
                return await asyncio.to_thread(func, *args, **kwargs)
            except openai.RateLimitError:
                if retry == self._max_retries - 1:
                    logger.error(f"OpenAI Rate Limit failed after {self._max_retries} attempts")
                    raise Exception("Exceeded max retries due to rate limiting.")
                
                await asyncio.sleep(backoff_time)
                backoff_time *= self._retry_backoff_multiplier
            except Exception as e:
                logger.error(f"Critical OpenAI failure: {str(e)}")
                raise e
            
    def _param_or_default(self, value, default):
        return value if value is not None else default

    
    

