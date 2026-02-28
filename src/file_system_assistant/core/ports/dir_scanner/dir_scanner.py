from typing import Protocol, runtime_checkable

from file_system_assistant.adapters.file_io.file_ext_type import FileExt
from file_system_assistant.core.ports.common.models.file_metadata import FileMetadata


@runtime_checkable
class DirScanner(Protocol):

    def list_dir(self, dirpath: str, file_extension: FileExt | None) -> list[FileMetadata]:
        ...
