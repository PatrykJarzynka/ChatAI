import jwt
from fastapi import HTTPException, status
from functools import wraps

from interfaces.exceptions import EmptyFileError, InvalidFileSizeError, UnsupportedExtensionError, UnsupportedMimeTypeError

class FileExceptionHandler:
    def handle_file_exceptions(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except EmptyFileError as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Empty file.')
            except UnsupportedExtensionError as e:
                raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail='Unsupported extension!')
            except UnsupportedMimeTypeError as e:
                raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail='Unsupporetd mime type!')
            except InvalidFileSizeError as e:
                raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail='File size is too big!')
            except ValueError as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
            except HTTPException as e:
                raise e
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        return wrapper