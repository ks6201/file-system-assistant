

from dataclasses import dataclass

@dataclass(frozen=True)
class Constants:
    QUIT = "quit"
    EXIT = "exit"
    LOGGER_NAME = "fsa-logger"
    LOGS_PATH = "logs/prompt.log"
    GOOGLE_API_KEY_ENV = "GOOGLE_API_KEY"
    OPENAI_API_KEY_ENV = "OPENAI_API_KEY"