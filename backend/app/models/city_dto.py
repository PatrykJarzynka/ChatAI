from pydantic import BaseModel

class CityDTO(BaseModel):
    city: str