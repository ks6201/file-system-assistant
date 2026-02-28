

from enum import StrEnum

from file_system_assistant.adapters.llms.gemini.gemini_llm import GeminiLLM
from file_system_assistant.adapters.llms.openai.openai_llm import OpenAILLM
from file_system_assistant.app.services.container import Container
from file_system_assistant.core.ports.llm.llm import LLM
from file_system_assistant.core.ports.tools_registry.tools_registry import ToolsRegistry


class LLMProvider(StrEnum):
    GEMINI = "gemini"
    OPENAI = "openai"


class LLMFactory:

    @staticmethod
    def create(llm: LLMProvider) -> LLM:

        tools_registry = Container.resolve(ToolsRegistry)

        match llm:
            case LLMProvider.GEMINI:
                return GeminiLLM(tools_registry)
            case LLMProvider.OPENAI:
                return OpenAILLM(tools_registry)