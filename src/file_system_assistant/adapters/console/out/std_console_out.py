


import os
import sys

from file_system_assistant.app.ports.console_out import ConsoleOut


class StdConsoleOut(ConsoleOut):

    def write_line(self, *values: object) -> None:
        print(*values)
        
    def write_block(self, *values: object) -> None:
        print()
        print(*values)
        print()

    def write_error(self, *values: object) -> None:
        print(*values, file=sys.stderr)

    def write_error_block(self, *values: object) -> None:
        print()
        self.write_error(*values)
        print()

    def flush(self) -> None:
        sys.stdout.flush()

    def clear_screen(self) -> None:
        os.system("cls" if os.name == "win" else "clear")