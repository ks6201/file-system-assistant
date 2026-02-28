from typing import Any

from file_system_assistant.adapters.file_io.file_ext_type import is_file_ext_type
from file_system_assistant.app.services.container import Container
from file_system_assistant.core.ports.dir_scanner.dir_scanner import DirScanner
from file_system_assistant.core.ports.tools_registry.tools_registry import Tool
from file_system_assistant.core.tools.tool_response import SuccessResponse, tool_response

from file_system_assistant.core.ports.common.models.file_metadata import FileMetadata


@tool_response
def dir_scanner(
    dirpath: str,
    extension: str | None = None
) -> SuccessResponse[list[FileMetadata]]:
    """
    Scan a directory and return metadata for matching files.

    The returned value is a dictionary representation of a
    `SuccessResponse[list[FileMetadata]]` dataclass instance.
    The conversion is performed by the `transform_response` decorator
    using `dataclasses.asdict()`.

    Args:
        dirpath (str):
            Path of the directory to scan.

        extension (str | None, optional):
            Optional file extension filter (e.g., ".txt").
            If provided, only files matching this extension are included.

    Returns:
        dict[str, Any]:
            A dictionary produced from the underlying
            `SuccessResponse[list[FileMetadata]]` dataclass.
            The exact structure depends on the fields defined
            in `SuccessResponse`.

    Raises:
        FileNotFoundError:
            If `dirpath` does not exist.

        PermissionError:
            If access to the directory is denied.
    """
    
    scanner = Container.resolve(DirScanner)

    ext = extension if is_file_ext_type(extension) else None
    
    result = scanner.list_dir(dirpath, ext)

    resp = SuccessResponse(result)
    return resp


from typing import Any

dir_scanner_tool_schema: dict[str, Any] = {
    "type": "function",
    "name": "dir_scanner_tool",
    "description": (
        "Scan a directory and return metadata for files inside it.\n\n"
        "Use this tool when the user wants to:\n"
        "- List files in a directory\n"
        "- Filter files by extension (e.g., '.txt')\n"
        "- Inspect file metadata\n\n"
        "Requires a directory path. Optionally filters by file extension."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "dirpath": {
                "type": "string",
                "description": "Absolute or relative path of the directory to scan"
            },
            "extension": {
                "type": "string",
                "description": "Optional file extension including leading dot, e.g. '.txt'"
            }
        },
        "required": ["dirpath"]
    }
}

dir_scanner_tool = Tool(dir_scanner, dir_scanner_tool_schema)