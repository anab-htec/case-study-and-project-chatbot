from typing import TypeVar, Generic, List
from pydantic import BaseModel

from app.models.vector_search_result import VectorSearchResult

T = TypeVar("T")

class WeightedSearchResult(BaseModel, Generic[T]):
    results: List[VectorSearchResult[T]]
    weight: float