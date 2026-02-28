from file_system_assistant.adapters.file_io.docx_file_io import DocxFileIO
from file_system_assistant.adapters.file_io.file_ext_type import FileExt
from file_system_assistant.adapters.file_io.pdf_file_io import PyMuPdfFileIO
from file_system_assistant.adapters.file_io.text_file_io import StdTextFileIO
from file_system_assistant.core.ports.file_io.file_io import FileIO
from file_system_assistant.adapters.file_io.binary_file_io import StdBinaryFileIO

class FileIOFactory:

    @staticmethod
    def create(file_ext: FileExt) -> FileIO:
        match file_ext:
            case "pdf":
                return PyMuPdfFileIO()
            case "docx":
                return DocxFileIO()
            case ("txt" | "md"):
                return StdTextFileIO()
            case _:
                return StdBinaryFileIO()