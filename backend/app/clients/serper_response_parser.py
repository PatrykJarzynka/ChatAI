from typing import Dict, Any, List
from llama_index.core import Document
from interfaces.web_response_parser import WebResponseParser

class SerperResponseParser(WebResponseParser):

    def extract_answer(self, data: Dict[str, Any]) -> List[Document]:
        if "snippet" in data['answerBox']:
            return [Document(text=data['answerBox']["snippet"], metadata={"url": data['answerBox']["link"]})]
        else:
            return [Document(text=data['answerBox']['answer'])]

    def parse(self, data: Dict[str, Any]) -> List[Document]:
        if "answerBox" in data:
            return self.extract_answer(data)
        
        return [Document(text=item["snippet"], metadata={"url": item["link"]}) for item in data["organic"]]