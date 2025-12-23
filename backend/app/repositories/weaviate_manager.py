from typing import Optional
import weaviate
from weaviate import WeaviateAsyncClient

from app.core.config import settings
from app.repositories.interfaces.project_repo import ProjectRepository
from app.repositories.interfaces.case_study_repo import CaseStudyRepository
from app.repositories.weaviate_project_repo import WeaviateProjectRepository
from app.repositories.weaviate_case_study_repo import WeaviateCaseStudyRepository

class WeaviateManager:

    def __init__(self):
        self._host = settings.WEAVIATE_HOST
        self._client: Optional[WeaviateAsyncClient] = None

    async def connect(self):
        if self._client is None:
            self._client = weaviate.use_async_with_local(host=self._host)
            await self._client.connect()
        return self._client
    
    async def disconnect(self):
        if self._client:
            await self._client.close()
            self._client = None

    def get_client(self) -> WeaviateAsyncClient:
        if self._client is None:
            raise RuntimeError("Weaviate client is not connected")
        return self._client

    def get_project_repo(self) -> ProjectRepository:
        return WeaviateProjectRepository(client=self.get_client())
    
    def get_case_study_repo(self) -> CaseStudyRepository:
        return WeaviateCaseStudyRepository(client=self.get_client())