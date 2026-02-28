from dataclasses import dataclass
from datetime import datetime

from file_system_assistant.adapters.file_io.file_ext_type import FileExt

@dataclass
class FileMetadata:
    name: str
    size: int
    kind: FileExt
    modified_date: str

    def __init__(
        self,
        name: str,
        size: int,
        kind: FileExt,
        modified_date: datetime
    ):
        self.name = name
        self.size = size
        self.kind = kind
        self.modified_date = modified_date.isoformat()