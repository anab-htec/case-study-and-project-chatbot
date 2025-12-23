from typing import List, Optional, Literal, Union
from pydantic import BaseModel

from app.models.constants import WorfklowStatus
from app.models.project import Project
from app.models.case_study import CaseStudy
from app.models.scored_record import ScoredRecord

class ChatResponse(BaseModel):
    workflow_id: Optional[str]
    status: WorfklowStatus
    response: str
    context: Union[List[ScoredRecord[Project]], List[ScoredRecord[CaseStudy]], None] = None

