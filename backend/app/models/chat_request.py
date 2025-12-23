from typing import Optional
from pydantic import BaseModel

class ChatRequest(BaseModel):
    workflow_id: Optional[str]
    query: str