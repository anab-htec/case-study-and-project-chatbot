from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")

class ScoredRecord(BaseModel, Generic[T]):
    record: T
    score: float