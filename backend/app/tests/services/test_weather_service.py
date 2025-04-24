import pytest
from clients.weather_service import WeatherService
from unittest.mock import patch
from models.weather_api_response import WeatherApiResponse
from models.state_dto import StateDTO
from models.city_dto import CityDTO
from models.city_data_dto import CityDataDTO
from utilities.open_ai_helper import OpenAIHelper
from typing import List

@pytest.fixture
def weather_service():
    return WeatherService()

def run_get_city_weather_data_test(provider: WeatherService, city: str, country: str, supported_cities: List[str]):
    mocked_supported_cities = map(lambda city: {"city": city}, supported_cities)

    mocked_states_response: WeatherApiResponse[StateDTO] = {
        "status": 'success',
        "data": [
            {"state":"Silesia"},
            {"state":"Greater Poland"},
            {"state":"Kujawsko-Pomorskie"}
        ]
    }

    mocked_cities_response: WeatherApiResponse[CityDTO] = {
        "status": 'success',
        "data": mocked_supported_cities
    }

    mock_state = mocked_states_response['data'][0]['state']
    expected_states = list(map(lambda data: data['state'], mocked_states_response['data']))

    with patch.object(provider, 'get_supported_states', return_value=mocked_states_response) as mock_get_supported_states, \
        patch.object(provider, 'get_supported_cities_in_state', return_value=mocked_cities_response) as mock_mocked_cities_response, \
        patch.object(OpenAIHelper, 'get_state_assigned_to_city' ,return_value=mock_state) as mock_get_state_assigned_to_city:
            result = provider.get_city_weather_data(city, country)

    mock_get_supported_states.assert_called_with(country),
    mock_get_state_assigned_to_city.assert_called_once_with(city, expected_states)
    mock_mocked_cities_response.assert_called_with(country, mock_state)

    return result

def test_get_city_weather_data(weather_service: WeatherService):
    supported_cities = ['Gliwice', 'Katowice', 'Rybnik']
    mocked_city = supported_cities[0]
    mocked_state = 'Silesia'
    mocked_country = 'Poland'

    mocked_city_data: WeatherApiResponse[CityDataDTO] = {
         "status": 'success',
         "data": [
              {
                "city": mocked_city,
                "state": mocked_state,
                "country": mocked_country,
                "location": {
                    "type": 'Point',
                    "coordinates": [
                        18.516138055555555,
                        50.111179444444446
                    ]
                },
                "current": {
                    "pollution": {
                        "ts": "2025-04-24T09:00:00.000Z",
                        "aqius": 62,
                        "mainus": "p2",
                        "aqicn": 25,
                        "maincn": "o3"
                    },
                    "weather": {
                        "ts": "2025-04-24T09:00:00.000Z",
                        "tp": 19,
                        "pr": 1010,
                        "hu": 65,
                        "ws": 1.79,
                        "wd": 355,
                        "ic": "04d"
                    }
              } 
            }                 
        ]
    }

    with patch.object(weather_service, 'get_city_data', return_value=mocked_city_data) as mock_get_city_data:
        result = run_get_city_weather_data_test(weather_service, mocked_city, mocked_country, supported_cities)
    
    mock_get_city_data.assert_called_once_with(mocked_city, mocked_state, mocked_country)
    assert result == mocked_city_data


def test_get_not_supported_city_weather_data(weather_service: WeatherService):
    supported_cities = ['Gliwice', 'Katowice', 'Rybnik']
    mocked_city = 'Żory'
    mocked_country = 'Poland'


    result = run_get_city_weather_data_test(weather_service, mocked_city, mocked_country, supported_cities)
    assert result == 'City not supported. Try to use web_search_tool to find answer.'