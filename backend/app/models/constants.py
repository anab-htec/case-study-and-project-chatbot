from enum import Enum

class Intent(str, Enum):
    PROJECT_MATCHING = "project_matching"
    CASE_STUDY_RETRIEVAL = "case_study_retrieval"
    AMBIGUOUS = "ambiguous"

class FailureReason(str, Enum):
    AMBIGUOUS_INTENT = "ambiguous_intent"
    NO_MATCHING_RECORDS = "no_matching_records"

class WorfklowStatus(str, Enum):
    COMPLETED = "completed"
    CLARIFICATION_REQUIRED = "clarification_required"
    FAILED = "failed"