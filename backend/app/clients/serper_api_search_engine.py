from interfaces.web_manager import WebManager
from typing import Dict
import requests

class SerperApiSearchEngine(WebManager):

    def __init__(self, api_key: str):
        self.endpoint = "https://google.serper.dev/search"
        self.api_key = api_key

    def search_web(self, query: str):
        payload = {
            "q": query,
            "gl": "pl",
        }

        search_results = requests.post(
            url=self.endpoint,
            json=payload,
            headers={"X-API-KEY": self.api_key}
        )

        return search_results.json()