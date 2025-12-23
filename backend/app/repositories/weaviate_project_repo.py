from typing import Dict, List
from weaviate import WeaviateAsyncClient
from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.query import MetadataQuery

from app.models.project import Project
from app.models.vector_search_result import VectorSearchResult
from app.repositories.interfaces.project_repo import ProjectRepository

class WeaviateProjectRepository(ProjectRepository):
    COLLECTION_NAME = "Project"

    def __init__(self, client: WeaviateAsyncClient):
        self._client = client

    async def create_schema(self) -> None:
        exists = await self._client.collections.exists(self.COLLECTION_NAME)
        if exists:
            await self._client.collections.delete(self.COLLECTION_NAME)
        
        await self._client.collections.create(
            self.COLLECTION_NAME,
            properties = [
                Property(name="title", data_type=DataType.TEXT),
                Property(name="techStack", data_type=DataType.TEXT_ARRAY),
                Property(name="solutionsImplemented", data_type=DataType.TEXT_ARRAY),
                Property(name="servicesOffered", data_type=DataType.TEXT_ARRAY),
                Property(name="summary", data_type=DataType.TEXT)
            ],
            vector_config=[
                Configure.Vectors.self_provided(
                    name="technicalVector"
                ),
                Configure.Vectors.self_provided(
                    name="serviceVector"
                )
            ]
        )

    async def insert_project(self, properties: Dict[str, any], vector_data: Dict[str, List[float]]) -> None:
        collection = self._client.collections.get(self.COLLECTION_NAME)

        await collection.data.insert(
            properties = properties,
            vector = vector_data
        )

    async def retrieve_project_records_by_technical_vector(self, vector, top_k) -> List[VectorSearchResult[Project]]:
        return await self.retrieve_project_records(vector, "technicalVector", top_k)

    async def retrieve_project_records_by_service_vector(self, vector, top_k) -> List[VectorSearchResult[Project]]:
        return await self.retrieve_project_records(vector, "serviceVector", top_k)

    async def retrieve_project_records(self, vector, vector_name, top_k) -> List[VectorSearchResult[Project]]:
        project_search_results: list[VectorSearchResult[Project]] = []
        collection = self._client.collections.get(self.COLLECTION_NAME)
        records = await collection.query.near_vector(
            near_vector = vector,
            limit = top_k,
            target_vector = vector_name,
            return_metadata = MetadataQuery(certainty=True)
        )

        for item in records.objects:
            props = item.properties

            project = Project(
                title = props["title"],
                techStack = props["techStack"],
                solutionsImplemented = props["solutionsImplemented"],
                servicesOffered = props["servicesOffered"],
                summary = props["summary"]
            )

            vector_search_result = VectorSearchResult[Project](
                id = str(item.uuid),
                obj = project,
                certainty = item.metadata.certainty
            )

            project_search_results.append(vector_search_result)

        return project_search_results