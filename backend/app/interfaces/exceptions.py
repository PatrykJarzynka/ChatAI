class EmptyFileError(ValueError):
    """File is empty."""

class UnsupportedExtensionError(ValueError):
    """File extension is not supported."""

class UnsupportedMimeTypeError(ValueError):
    """File mime type is not supported."""

class InvalidFileSizeError(ValueError):
    """File size is too big."""