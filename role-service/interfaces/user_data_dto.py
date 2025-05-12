from pydantic import BaseModel


class UserDataDTO(BaseModel):
    user_id: int