from abc import ABC, abstractmethod

from file_system_assistant.core.ports.llm.llm_input import LLMInput
from file_system_assistant.core.ports.tools_registry.tools_registry import ToolsRegistry
from file_system_assistant.core.types.result import Result
from .llm_response import LLMResponse

class LLM(ABC):

    def __init__(self, tools_registry: ToolsRegistry):
        self._tools_registry = tools_registry

    @abstractmethod
    def generate(self, llm_input: LLMInput) -> Result[LLMResponse, str]:
        ...

    @abstractmethod
    def close(self):
        ...