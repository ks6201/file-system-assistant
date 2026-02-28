

from dataclasses import dataclass
from enum import StrEnum

class LLMRole(StrEnum):
    SYSTEM = "system"
    DEVELOPER = "developer"
    USER = "user"
    ASSISTANT = "assistant"

@dataclass
class LLMInput:
    role: LLMRole
    content: str