

from typing import Optional, Protocol, runtime_checkable

from .types import Tool, Tools


@runtime_checkable
class ToolsRegistry(Protocol):

    def register(self, tool: Tool) -> None:
        ...

    def register_m(self, tools: list[Tool]) -> None:
        ...

    def tools(self) -> Tools:
        ...

    def get_tool(self, tool_name: str) -> Optional[Tool]:
        ...