from typing import Protocol


class AIProvider(Protocol):
    def summarize(self, text: str) -> str:
        pass


class FakeAIProvider:
    def summarize(self, text: str) -> str:
        return f"Summary: {text[:80]}"


class OpenAIProvider:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def summarize(self, text: str) -> str:
        # Real OpenAI call would go here.
        return "Read AI summary"
