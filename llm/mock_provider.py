from llm.base import LLMProvider

class MockProvider(LLMProvider):
    def generate(self, prompt: str) -> str:
        return """
        {
            "patient": {"age": 65, "sex": "male"},
            "diagnosis": "lung cancer",
            "findings": ["mass in right lung"],
            "treatment": null
        }
        """