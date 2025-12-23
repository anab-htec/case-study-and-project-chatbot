from typing import List

from app.models.record import Record

class Project(Record):
    techStack: List[str]
    solutionsImplemented: List[str]
    servicesOffered: List[str]
    summary: str