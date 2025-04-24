from pydantic import BaseModel

class StateDTO(BaseModel):
    state: str