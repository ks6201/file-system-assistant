
from typing import Any

from file_system_assistant.app.services.container import Container
from file_system_assistant.core.ports.file_content_searcher.file_content_searcher import FileContentSearcher
from file_system_assistant.core.ports.file_content_searcher.search_match import SearchMatch
from file_system_assistant.core.ports.tools_registry.tools_registry import Tool
from file_system_assistant.core.tools.tool_response import ErrorResponse, SuccessResponse, tool_response

@tool_response
def file_content_searcher(
    filepath: str,
    keyword: str
) -> SuccessResponse[SearchMatch] | ErrorResponse[str]:
    """
    Search a file for a keyword and return structured match details.

    The function returns either a `SuccessResponse[SearchMatch]`
    or an `ErrorResponse[str]` dataclass instance. The `tool_response`
    decorator converts the returned dataclass instance into a dictionary
    using `dataclasses.asdict()` before it is returned to the caller.

    Args:
        filepath (str):
            Path to the file to search.

        keyword (str):
            Case-insensitive search term to locate within the file.

    Returns:
        dict[str, Any]:
            Dictionary representation of either:

            • a success response containing a `SearchMatch` payload  
            • an error response containing an error message string

            The exact structure corresponds to the fields defined in
            `SuccessResponse` and `ErrorResponse`.

    Raises:
        FileNotFoundError:
            If `filepath` does not exist.

        PermissionError:
            If access to read the file is denied.
    """

    fcst = Container.resolve(FileContentSearcher)

    result = fcst.search_in_file(filepath, keyword)

    if result.is_err():
        return ErrorResponse(result.unwrap_err())

    return SuccessResponse(result.unwrap())


file_content_searcher_tool_schema: dict[str, Any] = {
    "type": "function",
    "name": "file_content_searcher_tool",
    "description": (
        "Search a file for a keyword and return structured match details.\n\n"
        "Use this tool when:\n"
        "- The user wants to search inside a specific file\n"
        "- The user provides a file path and a search term\n"
        "- A case-insensitive content search is required\n\n"
        "Returns structured match information or an error response."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "filepath": {
                "type": "string",
                "description": "Absolute or relative path to the file to search"
            },
            "keyword": {
                "type": "string",
                "description": "Case-insensitive search term to locate within the file"
            }
        },
        "required": ["filepath", "keyword"]
    }
}

file_content_searcher_tool = Tool(
    file_content_searcher, 
    file_content_searcher_tool_schema
)