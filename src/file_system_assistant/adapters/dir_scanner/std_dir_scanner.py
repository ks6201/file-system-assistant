


from datetime import datetime
from logging import Logger
import os
from typing import cast

from file_system_assistant.adapters.file_io.file_ext_type import FileExt
from file_system_assistant.app.services.container import Container
from file_system_assistant.core.ports.common.models.file_metadata import FileMetadata
from file_system_assistant.core.ports.dir_scanner.dir_scanner import DirScanner

class StdDirScanner(DirScanner):

    def __init__(self) -> None:
        super().__init__()
        self.logger = Container.resolve(Logger)

    def list_dir(self, dirpath: str, file_extension: FileExt | None) -> list[FileMetadata]:
        try:
            entries = os.listdir(dirpath)
        except FileNotFoundError as e:
            self.logger.error(e)
            return []

        result: list[FileMetadata] = []

        for file in entries:
            if file_extension is not None and not file.endswith(file_extension):
                continue

            path = os.path.join(dirpath, file)
            if not os.path.isfile(path):
                continue

            stat = os.stat(path)

            result.append(
                FileMetadata(
                    name=file,
                    kind=cast(FileExt, file_extension if file_extension else os.path.splitext(file)[1]),
                    modified_date=datetime.fromtimestamp(stat.st_mtime),
                    size=stat.st_size,
                )
            )

        return result