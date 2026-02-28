

from rich.markdown import Markdown
from rich.console import Console as MdConsole
from file_system_assistant.app.ports.console_out import ConsoleOut


class MarkdownConsoleOut(ConsoleOut):

    def __init__(self) -> None:
        self.__stdout = MdConsole()
        self.__stderr = MdConsole(stderr=True)

    def _render(self, console: MdConsole, *values: object) -> None:
        for value in values:
            if isinstance(value, str):
                console.print(Markdown(value))
            else:
                console.print(value)

    def write_line(self, *values: object) -> None:
        self._render(self.__stdout, *values)

    def write_block(self, *values: object) -> None:
        self.__stdout.print()
        self._render(self.__stdout, *values)
        self.__stdout.print()

    def write_error(self, *values: object) -> None:
        self._render(self.__stderr, *values)

    def write_error_block(self, *values: object) -> None:
        self.__stderr.print()
        self._render(self.__stderr, *values)
        self.__stderr.print()

    def flush(self) -> None:
        self.__stdout.file.flush()
        self.__stderr.file.flush()

    def clear_screen(self) -> None:
        self.__stdout.clear()