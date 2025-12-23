from typing import Dict, List
from weaviate import WeaviateAsyncClient
from weaviate.classes.config import Property, DataType
from weaviate.classes.query import MetadataQuery

from app.models.case_study import CaseStudy
from app.models.vector_search_result import VectorSearchResult
from app.repositories.interfaces.case_study_repo import CaseStudyRepository

class WeaviateCaseStudyRepository(CaseStudyRepository):
    COLLECTION_NAME = "CaseStudy"

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
                Property(name="industry", data_type=DataType.TEXT),
                Property(name="technologies", data_type=DataType.TEXT_ARRAY),
                Property(name="solutionsProvided", data_type=DataType.TEXT_ARRAY),
                Property(name="services", data_type=DataType.TEXT_ARRAY),
                Property(name="detailedContent", data_type=DataType.TEXT),
                Property(name="sourceUrl", data_type=DataType.TEXT)
            ],
            vector_config=None
        )

    async def insert_case_study(self, properties: Dict[str, any], vector: List[float]) -> None:
        collection = self._client.collections.get(self.COLLECTION_NAME)

        await collection.data.insert(
            properties = properties,
            vector = vector
        )

    async def retrieve_case_study_records(self, vector, top_k) -> List[VectorSearchResult[CaseStudy]]:
        case_studies_search_results: list[VectorSearchResult[CaseStudy]] = []
        collection = self._client.collections.get(self.COLLECTION_NAME)
        records = await collection.query.near_vector(
            near_vector = vector,
            limit = top_k,
            target_vector = "default",
            return_metadata = MetadataQuery(certainty=True)
        )

        for item in records.objects:
            props = item.properties

            case_study = CaseStudy(
                title = props["title"],
                industry = props["industry"],
                technologies = props["technologies"],
                solutionsProvided = props["solutionsProvided"],
                services = props["services"],
                detailedContent = props["detailedContent"],
                sourceUrl = props["sourceUrl"]
            )

            vector_search_result = VectorSearchResult[CaseStudy](
                id = str(item.uuid),
                obj = case_study,
                certainty = item.metadata.certainty
            )

            case_studies_search_results.append(vector_search_result)

        return case_studies_search_results