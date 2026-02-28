from typing import Protocol, runtime_checkable
from file_system_assistant.core.types.result import Result

from .file_read_result import FileReadResult

@runtime_checkable
class FileIO(Protocol):
    
    def read_file(self, filepath: str) -> Result[FileReadResult, str]:
        ...

    def write_file(self, filepath: str, content: str | bytes) -> Result[bool, str]:
        ...