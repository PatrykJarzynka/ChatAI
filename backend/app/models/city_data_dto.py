from pydantic import BaseModel
from typing import List

class Location(BaseModel):
    type: str
    coordinates: List[float]

class Pollution(BaseModel):
    ts: str
    aquis: int
    mainus: str
    aqicn: int
    maincn: str


class Weather(BaseModel):
    ts: str
    tp: int
    pr: int
    hu: int
    ws: float
    wd: int
    ic: str

class CurrentData(BaseModel):
    pollution: Pollution
    weather: Weather

class CityDataDTO(BaseModel):
    city: str
    state: str
    country: str
    location: Location
    current: CurrentData