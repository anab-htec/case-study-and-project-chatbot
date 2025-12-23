from typing import List

from app.models.record import Record

class CaseStudy(Record):
    industry: str
    technologies: List[str] 
    solutionsProvided: List[str]
    services: List[str]
    detailedContent: str
    sourceUrl: str