from deepeval.test_case import LLMTestCase
from deepeval.metrics import BaseMetric

class RetrievalThresholdMetric(BaseMetric):
    def __init__(self, threshold: float = 1.0):
        self.threshold = threshold
        self.success = False 

    def measure(self, test_case: LLMTestCase):
        scores = test_case.additional_metadata.get("similarity_scores", [])
        
        if not scores:
            self.score = 0
            self.reason = "No similarity scores found in metadata."
            return self.score

        low_scores = [s for s in scores if s < 0.6]
        
        if len(low_scores) == 0:
            self.score = 1.0
            self.reason = f"All {len(scores)} projects met the 0.6 threshold."
        else:
            self.score = 1.0 - (len(low_scores) / len(scores))
            self.reason = f"{len(low_scores)} projects fell below the 0.6 threshold: {low_scores}"
        
        return self.score

    async def a_measure(self, test_case: LLMTestCase):
        return self.measure(test_case)

    def is_successful(self):
        return self.score >= self.threshold

    @property
    def __name__(self):
        return "Project Score Threshold"