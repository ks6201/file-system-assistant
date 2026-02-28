from logging import Logger
from pathlib import Path
from typing import Any, cast

from file_system_assistant.app.services.container import Container
from file_system_assistant.core.ports.file_io.file_read_result import FileReadResult
from file_system_assistant.core.ports.tools_registry.tools_registry import Tool
from file_system_assistant.core.tools.tool_response import ErrorResponse, SuccessResponse, tool_response

from file_system_assistant.adapters.file_io.file_io_factory import FileIOFactory
from file_system_assistant.adapters.file_io.file_ext_type import SUPPORTED_FILE_IO_TYPES, FileExt


def get_supported_file_io_types() -> dict[str, Any]:
    """
    Return the file types supported by `FileIOFactory` for
    read and write operations.

    Returns:
        dict[str, Any]:
            A dictionary with a single key:

            {
                "types": list[FileExt]
            }

            The value is the list of registered file extension
            types supported by the system. If no types are
            registered, the list will be empty.
    """

    return {
        "types": SUPPORTED_FILE_IO_TYPES
    }


get_supported_file_io_types_tool_schema: dict[str, Any] = {
    "type": "function",
    "name": "get_supported_file_io_types_tool",
    "description": (
        "Return the list of file extensions supported by the system "
        "for read and write operations.\n\n"
        "Use this tool when:\n"
        "- The user wants to know which file types are supported\n"
        "- Validation of allowed file extensions is needed\n"
        "- The system must determine compatible formats before reading or writing files\n\n"
        "Returns a list of supported file extension types."
    ),
    "parameters": {
        "type": "object",
        "properties": {},
        "required": []
    }
}


# ----


@tool_response
def read_file(
    filepath: str
) -> SuccessResponse[FileReadResult] | ErrorResponse[str]:
    """
    Read a file and return a structured representation of its contents.

    The function returns either a `SuccessResponse[FileReadResult]`
    or an `ErrorResponse[str]` dataclass instance. The `tool_response`
    decorator converts the returned dataclass instance into a dictionary
    using `dataclasses.asdict()` before returning it to the caller.

    Args:
        filepath (str):
            Absolute or relative path to the target file.

    Returns:
        dict[str, Any]:
            Dictionary representation of either:

            • a success response containing a `FileReadResult` payload  
            • an error response containing an error message string

            The exact structure corresponds to the fields defined in
            `SuccessResponse`, `ErrorResponse`, and `FileReadResult`.

    Raises:
        FileNotFoundError:
            If the file does not exist at the specified path.

        ValueError:
            If the file extension is not supported by `FileIOFactory`.

        PermissionError:
            If access to read the file is denied.
    """
    logger = Container.resolve(Logger)

    ext = Path(filepath).suffix.lstrip(".").lower()

    ftype = cast(FileExt, ext)

    try:
        reader = FileIOFactory.create(ftype)
    except (Exception, NotImplementedError) as e:
        logger.error(e)
        return ErrorResponse("Failed to read file")
    
    result = reader.read_file(filepath)

    if result.is_err():
        return ErrorResponse(result.unwrap_err())

    return SuccessResponse(result.unwrap())

read_file_tool_schema: dict[str, Any] = {
    "type": "function",
    "name": "read_file_tool",
    "description": (
        "Read a file and return a structured representation of its contents.\n\n"
        "Use this tool when:\n"
        "- The user wants to view or inspect the contents of a specific file\n"
        "- A file path is provided\n"
        "- The file content needs to be retrieved for further processing\n\n"
        "Returns structured file content information or an error response."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "filepath": {
                "type": "string",
                "description": "Absolute or relative path to the file to read"
            }
        },
        "required": ["filepath"]
    }
}


# --- 

@tool_response
def write_file(
    filepath: str,
    content: str
) -> SuccessResponse[str] | ErrorResponse[str]:
    """
    Write content to a file at the specified path.

    The function returns either a `SuccessResponse[str]`
    or an `ErrorResponse[str]` dataclass instance. The
    `tool_response` decorator converts the returned dataclass
    into a dictionary using `dataclasses.asdict()` before
    returning it to the caller.

    Args:
        filepath (str):
            Destination path where the file will be written.

        content (str):
            String content to write to the file.

    Returns:
        dict[str, Any]:
            Dictionary representation of either:

            • a success response containing a confirmation message (str)  
            • an error response containing an error message (str)

            The exact structure depends on the fields defined in
            `SuccessResponse` and `ErrorResponse`.

    Raises:
        OSError:
            If the filesystem prevents writing to the specified path.

        ValueError:
            If the file extension is not supported by `FileIOFactory`.

        PermissionError:
            If write access to the destination path is denied.
    """
    logger = Container.resolve(Logger)
    
    ext = Path(filepath).suffix.lstrip(".").lower()

    ftype = cast(FileExt, ext)

    try:
        writer = FileIOFactory.create(ftype)
    except (Exception, NotImplementedError) as e:
        logger.error(e)
        return ErrorResponse("File type not supported")

    result = writer.write_file(filepath, content)

    if result.is_err():
        return ErrorResponse(result.unwrap_err())
    
    return SuccessResponse("Write successful")


write_file_tool_schema: dict[str, Any] = {
    "type": "function",
    "name": "write_file_tool",
    "description": (
        "Write content to a file at the specified path.\n\n"
        "Use this tool when:\n"
        "- The user wants to create a new file\n"
        "- The user wants to overwrite or update an existing file\n"
        "- A file path and text content are provided\n\n"
        "Returns a confirmation message or an error response."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "filepath": {
                "type": "string",
                "description": "Destination path within the allowed working directory"
            },
            "content": {
                "type": "string",
                "description": "Text content to write into the file"
            }
        },
        "required": ["filepath", "content"]
    }
}


read_file_tool = Tool(read_file, read_file_tool_schema)
write_file_tool = Tool(write_file, write_file_tool_schema)
get_supported_file_io_types_tool = Tool(
    get_supported_file_io_types,
    get_supported_file_io_types_tool_schema
)