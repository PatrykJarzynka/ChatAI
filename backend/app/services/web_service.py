from interfaces.web_manager import WebManager
from interfaces.web_response_parser import WebResponseParser

class WebService:
    def __init__(self, web_manager: WebManager, parser: WebResponseParser):
        self.web_manager = web_manager
        self.parser = parser

    def provide_documents(self, query: str):
        data = self.web_manager.search_web(query)
        documents = self.parser.parse(data)
        return documents
