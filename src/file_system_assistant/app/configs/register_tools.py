


from file_system_assistant.app.services.container import Container
from file_system_assistant.core.ports.tools_registry.tools_registry import ToolsRegistry
from file_system_assistant.core.tools.dir_scanner_tool import dir_scanner_tool
from file_system_assistant.core.tools.file_io_tool import (
    read_file_tool,
    write_file_tool,
    get_supported_file_io_types_tool
)

from file_system_assistant.core.tools.file_content_searcher_tool import file_content_searcher_tool

def register_tools():
    
    registry = Container.resolve(ToolsRegistry)

    registry.register_m([
        read_file_tool,
        write_file_tool,
        get_supported_file_io_types_tool
    ])


    registry.register(dir_scanner_tool)

    registry.register(file_content_searcher_tool)