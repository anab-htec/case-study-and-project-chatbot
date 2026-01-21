from abc import ABC, abstractmethod
from typing import List, Optional

from app.models.record import Record

class LLMService(ABC):

    @abstractmethod
    async def generate_embedding(self, text) -> List[float]:
        pass

    @abstractmethod
    async def generate_text(self, 
        system_prompt: str, 
        user_message: str, 
        model: Optional[str] = None, 
        temperature: Optional[float] = None, 
        max_tokens: Optional[int] = None, 
        top_p: Optional[float] = None
    ) -> str:
        pass

    @abstractmethod
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
        pass
    