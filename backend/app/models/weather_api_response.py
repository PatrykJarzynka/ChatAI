from pydantic import BaseModel
from typing import List, Generic, TypeVar

T = TypeVar('T')  

class WeatherApiResponse(BaseModel, Generic[T]):
    status: str
    data: T

class WeatherApiResponseListData(BaseModel, Generic[T]):
    status: str
    data: List[T]