from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCaseParams

from evaluation.evaluation_llm import EvaluationLLM

evaluation_llm = EvaluationLLM()

no_results_clarification_metric = GEval(
    name="No results clarification metric",
    model=evaluation_llm,
    criteria=(
        "PASS (1.0) if the output explicitly states that no relevant records were found "
        "and does NOT provide any project/case study details or fabricated information.\n"
        "FAIL (0.0) otherwise."
    ),
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    threshold=1.0
)