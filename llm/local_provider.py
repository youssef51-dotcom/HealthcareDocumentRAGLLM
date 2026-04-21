import requests
from llm.base import LLMProvider


class LocalProvider(LLMProvider):
    def __init__(self, model="mistral"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def generate(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.0,
                "num_predict": 300  # limite réponse (important pour vitesse)
            }
        }

        try:
            response = requests.post(self.url, json=payload, timeout=1200)

            print("[DEBUG STATUS]", response.status_code)

            if response.status_code != 200:
                return ""

            return response.json().get("response", "")

        except Exception as e:
            print("[LLM ERROR]", str(e))
            return ""