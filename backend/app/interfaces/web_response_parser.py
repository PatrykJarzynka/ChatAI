from abc import ABC, abstractmethod
from typing import List, Dict, Any
from llama_index.core import Document

class WebResponseParser(ABC):

    @abstractmethod
    def parse(self, data: Dict[str, Any]) -> List[Document]:
        pass