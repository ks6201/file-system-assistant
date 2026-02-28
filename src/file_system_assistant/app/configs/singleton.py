

from file_system_assistant.adapters.console._in.prompt_toolkit_console_in import PromptToolKitConsoleIn
from file_system_assistant.adapters.console.out.markdown_console_out import MarkdownConsoleOut
from file_system_assistant.adapters.dir_scanner.std_dir_scanner import StdDirScanner
from file_system_assistant.adapters.file_content_searcher.std_file_content_search import StdFileContentSearch
from file_system_assistant.adapters.file_io.file_io_factory import FileIOFactory
from file_system_assistant.adapters.tools_registry.basic_tool_registry import BasicToolsRegistry
from file_system_assistant.app.ports.console_in import ConsoleIn
from file_system_assistant.app.ports.console_out import ConsoleOut
from file_system_assistant.app.services.container import Container
from file_system_assistant.core.ports.dir_scanner.dir_scanner import DirScanner
from file_system_assistant.core.ports.file_content_searcher.file_content_searcher import FileContentSearcher
from file_system_assistant.core.ports.tools_registry.tools_registry import ToolsRegistry
from file_system_assistant.app.services.container import Container


def register_singletons():
    
    Container.singleton(
        DirScanner, 
        lambda: StdDirScanner()
    )

    Container.singleton(
        FileIOFactory,
        lambda: FileIOFactory
    )

    Container.singleton(
        FileContentSearcher,
        lambda: StdFileContentSearch()
    )

    Container.singleton(
        ToolsRegistry,
        lambda: BasicToolsRegistry()
    )

    Container.singleton(
        ConsoleIn,
        lambda: PromptToolKitConsoleIn()
    )

    Container.singleton(
        ConsoleOut,
        lambda: MarkdownConsoleOut()
    )