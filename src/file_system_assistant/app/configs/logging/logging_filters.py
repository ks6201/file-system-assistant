import logging

class ConsoleOnlyFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return getattr(record, "console", False)