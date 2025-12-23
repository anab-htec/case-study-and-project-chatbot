from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCaseParams
from evaluation.evaluation_llm import EvaluationLLM

evaluation_llm = EvaluationLLM()

clarification_metric = GEval(
    name="Clarification metric",
    model=evaluation_llm,
    criteria=(
        "Determine if the assistant correctly handles out-of-scope or ambiguous inputs. "
        "The assistant SHOULD NOT answer questions unrelated to projects/case studies."
        "Instead, it must ask whether the user intends to retrieve projects or case studies or admit no results as per the expected behavior.. "
        "A high score is given if the ACTUAL_OUTPUT matches the intent of the EXPECTED_OUTPUT refusal."
    ),
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.EXPECTED_OUTPUT],
    threshold=0.7
)