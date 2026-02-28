from typing import Protocol, runtime_checkable

from file_system_assistant.core.types.result import Result

from .search_match import SearchMatch

@runtime_checkable
class FileContentSearcher(Protocol):
    def search_in_file(self, filepath: str, keyword: str) -> Result[SearchMatch, str]:
        ...