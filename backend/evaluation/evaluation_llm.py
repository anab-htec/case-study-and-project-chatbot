from openai import OpenAI
from deepeval.models.base_model import DeepEvalBaseLLM

from app.core.config import settings

class EvaluationLLM(DeepEvalBaseLLM):
    def __init__(self):
        self.model_name = settings.OPENAI_EVAL_MODEL
        self.temperature = settings.OPENAI_EVAL_TEMPERATURE
        self.max_tokens = settings.OPENAI_EVAL_MAX_TOKENS
        self.top_p = settings.OPENAI_EVAL_TOP_P
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY, 
            base_url=settings.OPENAI_BASE_URL
        )

    def load_model(self):
        return self.client

    def generate(self, prompt: str) -> str:
        chat_model = self.load_model()
        response = chat_model.chat.completions.create(
            model=self.model_name,           
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            messages=[{"role": "user", "content": prompt},]
        )
        return response.choices[0].message.content

    async def a_generate(self, prompt: str) -> str:
        return self.generate(prompt)

    def get_model_name(self):
        return self.model_name