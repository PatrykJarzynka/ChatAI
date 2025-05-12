from config import get_settings
import requests
from typing import Annotated
from utilities.open_ai_helper import OpenAIHelper
from models.weather_api_response import WeatherApiResponse
from models.state_dto import StateDTO
from models.city_dto import CityDTO
from models.city_data_dto import CityDataDTO

class WeatherService():

    def __init__(self):
        self.api_key = get_settings().AIR_API_KEY
        self.city_data_endpoint = get_settings().AIR_API_URL + '/city'
        self.supported_cities_endpoint = get_settings().AIR_API_URL + '/cities'
        self.supported_states_endpoint = get_settings().AIR_API_URL + '/states'
        

    def get_city_weather_data(self, city: Annotated[str,"Name of a city"], country: Annotated[str,"Name of a country"]):
        supported_states = list(map(lambda data: data.state, self.get_supported_states(country).data))
        
        state = OpenAIHelper().get_state_assigned_to_city(city, supported_states)
        supported_cities = list(map(lambda data: data.city, self.get_supported_cities_in_state(country, state).data)) 

        if city in supported_cities:
            return self.get_city_data(city, state, country)
        else:
            return "City not supported. Try to use web_search_tool to find answer."
        
    def get_supported_states(self, country: Annotated[str,"Name of a country"]) -> WeatherApiResponse[StateDTO]:
        params = {
            "country": country,
            "key": self.api_key
        }

        response = requests.get(self.supported_states_endpoint, params=params)
        return WeatherApiResponse[StateDTO](**response.json())
    
    def get_supported_cities_in_state(self, country: Annotated[str,"Name of a country"], state: Annotated[str,"Name of a state"]) -> WeatherApiResponse[CityDTO]:
        params = {
            "country": country,
            "state": state,
            "key": self.api_key
        }

        response = requests.get(self.supported_cities_endpoint, params=params)
        return WeatherApiResponse[CityDTO](**response.json())

    def get_city_data(self, city: Annotated[str,"Name of a city"] , state: Annotated[str,"Name of a state"], country: Annotated[str,"Name of a country"]) -> WeatherApiResponse[CityDataDTO]:
        """

        Response parameters should be interpeted as:
        - 'ts': time when data was gathered
        - 'aquis': AQI value based on US EPA standard
        - 'mainus': ain pollutant for US AQI
        - 'aqicn': AQI value based on China MEP standard
        - 'maincn': ain pollutant for Chinese AQI
        - 'tp': temperature in Celsius
        - 'pr': atmospheric pressure in hPa
        - 'hu': humidity %
        - 'ws': wind speed (m/s)
        - 'wd': wind direction, as an angle of 360° (N=0, E=90, S=180, W=270)
        - 'ic': icon code 
        
        """

        params = {
            "city": city,
            "state": state,
            "country": country,
            "key": self.api_key
        }

        response = requests.get(self.city_data_endpoint, params=params)
        return WeatherApiResponse[CityDataDTO](**response.json())