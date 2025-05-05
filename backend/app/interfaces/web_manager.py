from abc import ABC, abstractmethod
from typing import Dict, Any

class WebManager(ABC):
    
    @abstractmethod
    def search_web(self, query:str) -> Dict[str, Any]:
        pass