

from file_system_assistant.app.ports.console_in import ConsoleIn


class StdConsoleIn(ConsoleIn):

    def read_line(self, message: str) -> str:
        return input(message)