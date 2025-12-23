from abc import ABC, abstractmethod
from typing import List

from app.models.intent_context import IntentContext

class NLPProcessor(ABC):

    @abstractmethod
    async def process_query(self, query: str) -> IntentContext:
        pass

    async def condense_query(self, history: List[str]) -> str:
        pass
    