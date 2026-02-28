
from logging import Logger

import fitz
import os
from typing import cast
from datetime import datetime

from file_system_assistant.app.services.container import Container
from file_system_assistant.core.ports.file_io.file_io import FileIO
from file_system_assistant.core.ports.file_io.file_read_result import FileReadResult
from file_system_assistant.core.ports.common.models.file_metadata import FileMetadata
from file_system_assistant.core.types.result import Result

class PyMuPdfFileIO(FileIO):

    def __init__(self) -> None:
        super().__init__()
        self.logger = Container.resolve(Logger)

    def read_file(self, filepath: str) -> Result[FileReadResult, str]:
        try:
            with fitz.open(filepath) as doc:
                content = ""
                for page in doc:
                    text = cast(str, page.get_text("text")) # type: ignore
                    if not isinstance(text, str): # type: ignore
                        raise TypeError("Expected text output from get_text('text')")
                    content += text

                stats = os.stat(filepath)

                file_metadata = FileMetadata(
                    name=os.path.basename(filepath),
                    size=stats.st_size,
                    kind="pdf",
                    modified_date=datetime.fromtimestamp(stats.st_mtime),
                )
                
                result = FileReadResult(
                    is_binary=False,
                    content=content.strip(),
                    metadata=file_metadata,
                )

                return Result.ok(result)
        except Exception as e:
            self.logger.error(e)
            return Result.err("Failed to read PDF")


    def write_file(self, filepath: str, content: str | bytes) -> Result[bool, str]:
        try:
            text = ""

            if isinstance(content, bytes):
                text = content.decode("utf-8")
            elif isinstance(content, str):
                text = content

            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            if os.path.exists(filepath):
                doc = fitz.open(filepath)
            else:
                doc = fitz.open()
            page = doc.new_page()
            rect = fitz.Rect(72, 72, page.rect.width - 72, page.rect.height - 72)

            page.insert_textbox( # type: ignore
                rect,
                text,
                fontsize=12,
                fontname="helv",
                color=(0, 0, 0),
            )

            doc.save(cast(str, filepath)) # type: ignore
            doc.close()

            return Result.ok(True)
        
        except FileNotFoundError as e:
            self.logger.error(e)
            return Result.err("File not found")
        except Exception as e:
            self.logger.error(e)
            return Result.err("Something went wrong")