from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCaseParams

from evaluation.evaluation_llm import EvaluationLLM

evaluation_llm = EvaluationLLM()

def create_attribute_coverage_metric(target_attributes: list):
    attributes_str = ", ".join(target_attributes)

    return GEval(
        name="Attribute Capture",
        model=evaluation_llm,
        criteria=f"Determine if the summary captures at least 80% of the key attributes ({attributes_str}) from the source data.",
        evaluation_steps=[
            f"Identify all core entities for {attributes_str} in the retrieval_context",
            "Search the actual_output for these entities. A match is valid if the MEANING is the same, even if the language is more professional.",
            "Do NOT penalize for spelling corrections, capitalization changes, or standardizing informal terms into professional ones.",
            f"Calculate the coverage score: (Number of {attributes_str} captured / Total unique {attributes_str} in context).",
            "Score 1.0 if coverage is >= 80%, otherwise scale down proportionally."
        ],
        evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.RETRIEVAL_CONTEXT],
        threshold=0.8
    )