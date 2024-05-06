from openai import OpenAI
from config import getENV


class OpenAIClass:
    def __init__(self):
        self._client = OpenAI()
        self._client.api_key = getENV("OPENAI_API_KEY")

    def __call__(self):
        return self._client
