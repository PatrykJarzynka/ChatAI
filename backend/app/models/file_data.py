from pydantic import BaseModel

class FileData(BaseModel):
    file_name: str
    file_text: str
    file_extension: str