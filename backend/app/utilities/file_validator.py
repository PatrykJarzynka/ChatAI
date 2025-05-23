from fastapi import UploadFile

from interfaces.exceptions import UnsupportedMimeTypeError, InvalidFileSizeError

class FileValidator:

    def __init__(self) -> None:
        self.max_file_size = 2097152 # 2MB
        self.supported_content_types = ['text/plain','application/pdf']

    def validate_file(self, file: UploadFile) -> UploadFile:
        if (file.content_type not in self.supported_content_types):
            raise UnsupportedMimeTypeError('Unsupporetd mime type!')
        
        size = file.file.read()

        if len(size) > self.max_file_size:
            raise InvalidFileSizeError('File size is too big!')
        
        file.file.seek(0)
        
        return file

        

        