
from typing import Optional

from file_system_assistant.core.ports.tools_registry.tools_registry import ToolsRegistry
from file_system_assistant.core.ports.tools_registry.types import Tool, Tools


class BasicToolsRegistry(ToolsRegistry):

    def __init__(self) -> None:
        self.__tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        tool_name = tool.tool_schema["name"]
        self.__tools[tool_name] = tool

    def register_m(self, tools: list[Tool]) -> None:
        for tool in tools:
            self.register(tool)

    def tools(self) -> Tools:
        return tuple(self.__tools.values())
    
    def get_tool(self, tool_name: str) -> Optional[Tool]:
        tool = self.__tools.get(tool_name)
        
        return tool