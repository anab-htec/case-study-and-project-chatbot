from typing import TypeVar, Generic, Optional
from pydantic import BaseModel

T = TypeVar("T")

class VectorSearchResult(BaseModel, Generic[T]):
    id: str
    obj: T
    certainty: Optional[float] = None
