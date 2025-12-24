from deepeval.test_case import LLMTestCase
from deepeval.metrics import BaseMetric

class ScoreThresholdMetric(BaseMetric):
    def __init__(self, min_score: float = 0.6, threshold: float = 1.0):
        self.min_score = min_score
        self.threshold = threshold
        self.success = False 

    def measure(self, test_case: LLMTestCase):
        scores = test_case.additional_metadata.get("similarity_scores", [])
        
        if not scores:
            self.score = 0
            self.reason = "No similarity scores found in metadata."
            return self.score

        low_scores = [s for s in scores if s < self.min_score]
        
        if len(low_scores) == 0:
            self.score = 1.0
            self.reason = f"All {len(scores)} records met the {self.min_score} threshold."
        else:
            self.score = 1.0 - (len(low_scores) / len(scores))
            self.reason = f"{len(low_scores)} records fell below the {self.min_score} threshold: {low_scores}"
        
        return self.score

    async def a_measure(self, test_case: LLMTestCase):
        return self.measure(test_case)

    def is_successful(self):
        return self.score >= self.threshold

    @property
    def __name__(self):
        return "Score Threshold"