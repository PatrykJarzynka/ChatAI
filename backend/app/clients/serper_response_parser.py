from typing import Dict, Any, List
from llama_index.core import Document
from interfaces.web_response_parser import WebResponseParser

class SerperResponseParser(WebResponseParser):
    def parse(self, data: Dict[str, Any]) -> List[Document]:
        if "answerBox" in data:
            return [Document(text=data['answerBox']["snippet"], metadata={"url": data['answerBox']["link"]})]

        return [Document(text=item["snippet"], metadata={"url": item["link"]}) for item in data["organic"]]