from abc import ABC, abstractmethod
from typing import Dict, Any, List

from app.models.case_study import CaseStudy
from app.models.vector_search_result import VectorSearchResult

class CaseStudyRepository(ABC):

    @abstractmethod
    async def create_schema(self) -> None:
        pass

    @abstractmethod
    async def insert_case_study(self, properties: Dict[str, Any], vector: List[float]) -> None:
        pass

    @abstractmethod
    async def retrieve_case_study_records(self, vector, top_k) -> List[VectorSearchResult[CaseStudy]]:
        pass