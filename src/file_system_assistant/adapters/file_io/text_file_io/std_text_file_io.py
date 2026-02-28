

from datetime import datetime
from logging import Logger
import os

from file_system_assistant.app.services.container import Container
from file_system_assistant.core.ports.common.models.file_metadata import FileMetadata
from file_system_assistant.core.ports.file_io.file_io import FileIO
from file_system_assistant.core.ports.file_io.file_read_result import FileReadResult
from file_system_assistant.core.types.result import Result


class StdTextFileIO(FileIO):

    def __init__(self) -> None:
        super().__init__()
        self.logger = Container.resolve(Logger)

    def read_file(self, filepath: str) -> Result[FileReadResult, str]:
        try:
            stats = os.stat(filepath)

            file_metadata = FileMetadata(
                name=os.path.basename(filepath),
                size=stats.st_size,
                kind="txt",
                modified_date=datetime.fromtimestamp(stats.st_mtime),
            )
            
            with open(filepath, "r", encoding="utf-8") as reader:
                result = FileReadResult(
                    is_binary=False,
                    metadata=file_metadata,
                    content=reader.read()
                )

                return Result.ok(result)
        except Exception as e:
            self.logger.error(e)
            return Result.err(f"Failed to read text file")

    def write_file(self, filepath: str, content: str | bytes) -> Result[bool, str]:
        try:
            with open(filepath, "w", encoding="utf-8") as writer:

                if isinstance(content, str):
                    writer.write(content)
                elif isinstance(content, bytes):
                    writer.write(content.decode("utf-8"))
                else:
                    raise TypeError("content must be str or bytes")
        
            return Result.ok(True)
        
        except FileNotFoundError as e:
            self.logger.error(e)
            return Result.err("File not found")
        except Exception as e:
            self.logger.error(e)
            return Result.err("Something went wrong")