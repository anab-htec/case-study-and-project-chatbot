from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase

class IntentAccuracyMetric(BaseMetric):
    def __init__(self, threshold: float = 1.0):
        self.threshold = threshold
        self.score = 0
        self.reason = ""

    def measure(self, test_case: LLMTestCase):
        actual = test_case.additional_metadata.get("actual_intent")
        expected = test_case.additional_metadata.get("expected_intent")
        
        if actual is not None and actual == expected:
            self.score = 1.0
            self.reason = f"Correctly identified intent: {actual.name}"
        elif actual is None:
            self.score = 0.0
            self.reason = "Workflow failed to provide an intent_context."
        else:
            act_name = actual.name if actual else "None"
            exp_name = expected.name if expected else "None"
            self.score = 0.0
            self.reason = f"Intent Mismatch: Expected {exp_name} but got {act_name}."
        
        return self.score

    async def a_measure(self, test_case: LLMTestCase):
        return self.measure(test_case)

    def is_successful(self):
        return self.score >= self.threshold

    @property
    def __name__(self):
        return "Intent Accuracy"