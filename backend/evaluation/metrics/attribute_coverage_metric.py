import json
import re
from typing import List
from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase
from deepeval.models.base_model import DeepEvalBaseLLM

class AttributeCoverageMetric(BaseMetric):
    def __init__(self, model: DeepEvalBaseLLM, target_attributes: List[str], threshold: float = 0.8):
        self.model = model
        self.evaluation_model = getattr(model, "model_name", "Custom Model")
        self.target_attributes = target_attributes
        self.threshold = threshold
        self.score = 0
        self.success = False
        self.reason = ""

    def measure(self, test_case: LLMTestCase):
        entities=[]
        for context in test_case.retrieval_context:        
             for label in self.target_attributes:
                pattern = rf"{label}:\s*(.*?)(?=\n\s*[A-Z ]+:|$)"
                match = re.search(pattern, context, re.DOTALL | re.IGNORECASE)
                if match:
                    raw_text = match.group(1).strip()
                    items = [i.strip() for i in raw_text.split(",") if i.strip()]
                    entities.extend(items)

        if not entities:
            self.score = 1.0
            self.success = True
            self.reason = "No entites found in context."
            return self.score

        verification_prompt = f"""
        Summary: "{test_case.actual_output}"
        Entities to check: {entities}

        Check if each entity is mentioned in the summary. 
        Return ONLY a JSON object: {{"entity_name": true/false}}.
        Use 'true' if the meaning is present, even if rephrased.
        """
        
        response = self.model.generate(verification_prompt)

        try:
            json_str = re.search(r"\{.*\}", response, re.DOTALL).group()
            verdicts = json.loads(json_str)
            
            matched_count = sum(1 for present in verdicts.values() if present)
            total_count = len(entities)
            raw_coverage = matched_count / total_count

            self.success = raw_coverage >= self.threshold
            self.score = 1.0 if self.success else raw_coverage
            self.reason = f"Identified {matched_count}/{total_count} attributes."
            
        except Exception as e:
            self.score = 0
            self.success = False
            self.reason = f"Error during parsing: {str(e)}"

        return self.score
    
    async def a_measure(self, test_case: LLMTestCase):
        return self.measure(test_case)

    def is_successful(self):
        return self.score >= self.threshold

    @property
    def __name__(self):
        return "Attrubute Coverage"
   
    