

from typing import Protocol


class ConsoleIn(Protocol):

    def read_line(self, message: str) -> str:
        ...