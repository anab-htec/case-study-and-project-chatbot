from typing import List
from pydantic import BaseModel, Field

from app.models.constants import Intent

class IntentContext(BaseModel):
    """Unified schema for both intent classification and entity extraction."""
    
    intent: Intent = Field(
        description="Classify the query into one of the three strict categories."
    )

    justification: str = Field(
        description="Briefly explain why this intent was chosen based on the user's specific words."
    )

    technologies: List[str] = Field(
        description="List of specific technical requirements or technologies (e.g., 'Python', 'React')."
    )
    solutions: List[str] = Field(
        description="List of required business or technical solution keywords (e.g., 'CI/CD Pipeline', 'Risk Assessment')."
    )
    services: List[str] = Field(
        description="List of required service types or engagement models (e.g., 'Managed Service', 'Staff Augmentation')."
    )
    industry: List[str] = Field(
        description="List of industry verticals or domains (e.g., 'FinTech', 'Healthcare')."
    )