

import os

from file_system_assistant.adapters.llms.llm_factory import LLMProvider
from file_system_assistant.app.configs.constants import Constants


def select_llm_provider() -> LLMProvider:
    if os.getenv(Constants.OPENAI_API_KEY_ENV):
        return LLMProvider.OPENAI

    if os.getenv(Constants.GOOGLE_API_KEY_ENV):
        return LLMProvider.GEMINI

    raise RuntimeError(
        "No supported LLM provider API key found. "
        f"Set either '{Constants.OPENAI_API_KEY_ENV}' "
        f"or '{Constants.GOOGLE_API_KEY_ENV}' in the environment. "
        "Only one is required."
    )