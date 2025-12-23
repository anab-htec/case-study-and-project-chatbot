from abc import ABC, abstractmethod
from typing import List

from app.models.record import Record

class LLMService(ABC):

    @abstractmethod
    async def generate_embedding(self, text) -> List[float]:
        pass

    @abstractmethod
    async def generate_summary(self, query: str, system_prompt: str, user_prompt: str, records: List[Record]) -> str:
        pass

    @abstractmethod
    async def generate_text(self, system_prompt: str, user_message: str, temperature: float = 0.2, max_tokens: int = 500) -> str:
        pass

    @abstractmethod
    async def generate_object(self, system_prompt: str, user_message: str, response_format: type, temperature: float = 0.1, max_tokens: int = 500):
        pass
    