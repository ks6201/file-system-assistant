from dataclasses import dataclass

from file_system_assistant.core.ports.common.models.file_metadata import FileMetadata


@dataclass
class FileReadResult:
    is_binary: bool
    content: str | bytes
    metadata: FileMetadata