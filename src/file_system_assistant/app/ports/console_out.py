

from typing import Protocol

class ConsoleOut(Protocol):

    def write_line(self, *values: object) -> None: 
        ...

    def write_block(self, *values: object) -> None: 
        ...

    def write_error(self, *values: object) -> None:
        ...

    def write_error_block(self, *values: object) -> None:
        ...

    def flush(self) -> None:
        ...

    def clear_screen(self) -> None:
        ...