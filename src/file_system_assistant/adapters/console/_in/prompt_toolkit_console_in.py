

from prompt_toolkit import prompt
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory

from file_system_assistant.app.configs.constants import Constants
from file_system_assistant.app.ports.console_in import ConsoleIn


class PromptToolKitConsoleIn(ConsoleIn):

    def read_line(self, message: str) -> str:
        user_input = prompt(
            message,
            history=FileHistory(Constants.LOGS_PATH),
            auto_suggest=AutoSuggestFromHistory()
        )

        return user_input