from pydantic import BaseModel


class UserResponseDTO(BaseModel):
    id: int
    email: str
    full_name: str
