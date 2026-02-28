
from dataclasses import dataclass
from typing import Any, Callable

from file_system_assistant.core.tools.tool_response import ToolResponse


type ToolFn = Callable[..., ToolResponse]
type ToolSchema = dict[str, Any]

@dataclass
class Tool:
    tool_fn: ToolFn
    tool_schema: ToolSchema

type Tools = tuple[Tool, ...]
