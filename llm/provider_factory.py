from llm.openai_provider import OpenAIProvider
from llm.local_provider import LocalProvider
from llm.mock_provider import MockProvider


def get_provider(name: str):
    if name == "openai":
        return OpenAIProvider()

    elif name == "local":
        return LocalProvider(model="mistral")

    elif name == "mock":
        return MockProvider()

    else:
        raise ValueError(f"Unknown provider: {name}")