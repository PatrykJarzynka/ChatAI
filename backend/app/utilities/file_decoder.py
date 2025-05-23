import os

from fastapi import UploadFile

from interfaces.exceptions import EmptyFileError, UnsupportedExtensionError
from models.file_data import FileData

TXT = '.txt'
PDF = '.pdf'

class FileDecoder:

    def __init__(self) -> None:
        self.supported_extensions = [TXT,PDF]
    
    def get_file_data(self, file: UploadFile) -> FileData:
        if not file.filename:
            raise EmptyFileError('Empty file')
        
        file_text = ''
        file_name, file_extension = os.path.splitext(file.filename)

        if file_extension not in self.supported_extensions:
            raise UnsupportedExtensionError('Unsupported extension!')
        
        match file_extension:
            case ext if ext == TXT: 
                file_content = file.file.read()
                file_text = file_content.decode('utf-8')
            case ext if ext == PDF:
                file_text = 'test'
            
        return FileData(file_name=file_name, file_text=file_text, file_extension=file_extension)

                