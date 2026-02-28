

from logging import Logger

from file_system_assistant.app.services.container import Container
from file_system_assistant.core.ports.file_content_searcher.file_content_searcher import FileContentSearcher
from file_system_assistant.core.ports.file_content_searcher.search_match import SearchMatch
from file_system_assistant.core.types.result import Result


class StdFileContentSearch(FileContentSearcher):

    def __init__(self) -> None:
        super().__init__()
        self.logger = Container.resolve(Logger)
    
    def search_in_file(self, filepath: str, keyword: str) -> Result[SearchMatch, str]:
        lowered_keyword = keyword.lower()
        
        try:
            with open(filepath, "r") as file:
                for line_number, line in enumerate(file, start=1):
                    if lowered_keyword not in line: continue

                    result = SearchMatch(
                        context=line,
                        matched_text=keyword,
                        line_number=line_number
                    )

                    return Result.ok(result)
                
            return Result.err(f"No match found for '{keyword}'")
        except Exception as e:
            self.logger.error(e)
            return Result.err(f"Failed to read file")
        
