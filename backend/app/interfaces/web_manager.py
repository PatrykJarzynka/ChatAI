from abc import ABC, abstractmethod
from typing import Dict, Any

class WebManager(ABC):
    
    @abstractmethod
    def search_web(self) -> Dict[str, Any]:
        pass