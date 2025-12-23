from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase

class LatencyMetric(BaseMetric):
    def __init__(self, max_seconds: float = 40.0):
        self.max_seconds = max_seconds
        self.threshold = 1.0 

    def measure(self, test_case: LLMTestCase):
        latency = test_case.additional_metadata.get("latency", 0)
        
        if latency <= self.max_seconds:
            self.score = 1.0
            self.reason = f"Execution time of {latency:.2f}s is under the {self.max_seconds} seconds threshold."
        else:
            self.score = 0.0
            self.reason = f"Execution time of {latency:.2f}s is over the {self.max_seconds} seconds threshold."
        
        return self.score

    async def a_measure(self, test_case: LLMTestCase):
        return self.measure(test_case)

    def is_successful(self):
        return self.score == 1.0

    @property
    def __name__(self):
        return "Workflow Latency"