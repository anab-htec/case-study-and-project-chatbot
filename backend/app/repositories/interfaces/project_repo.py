from abc import ABC, abstractmethod
from typing import Dict, Any, List

from app.models.project import Project
from app.models.vector_search_result import VectorSearchResult

class ProjectRepository(ABC):

    @abstractmethod
    async def create_schema(self) -> None:
        pass

    @abstractmethod
    async def insert_project(self, properties: Dict[str, Any], vector_data: Dict[str, List[float]]) -> None:
        pass

    @abstractmethod
    async def retrieve_project_records_by_technical_vector(self, vector, top_k) -> List[VectorSearchResult[Project]]:
        pass

    @abstractmethod
    async def retrieve_project_records_by_service_vector(self, vector, top_k) -> List[VectorSearchResult[Project]]:
        pass