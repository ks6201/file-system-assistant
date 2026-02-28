
from typing import Any, Literal, TypeGuard

type FileExt = Literal["md", "txt", "pdf", "docx"]
SUPPORTED_FILE_IO_TYPES: list[FileExt] = [
    "md", "txt", "pdf", "docx"
]


def is_file_ext_type(value: Any) -> TypeGuard[FileExt]:
    if value is None or not isinstance(value, str):
        return False
 
    return value in SUPPORTED_FILE_IO_TYPES