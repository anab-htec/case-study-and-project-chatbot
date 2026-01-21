from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCaseParams

from evaluation.evaluation_llm import EvaluationLLM

evaluation_llm = EvaluationLLM()

ambiguous_intent_clarification_metric = GEval(
    name="Ambiguous intent clarification metric",
    model=evaluation_llm,
    criteria=(
        "PASS (1.0) if the output asks the user to clarify whether they are interested in projects or case studies "
        "and does NOT provide any project/case study details or fabricated information.\n"
        "FAIL (0.0) otherwise."
    ),
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    threshold=1.0
)