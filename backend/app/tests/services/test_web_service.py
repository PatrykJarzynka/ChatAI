import pytest
from services.web_service import WebService
from clients.serper_api_search_engine import SerperApiSearchEngine
from clients.serper_response_parser import SerperResponseParser
from unittest.mock import patch
from llama_index.core import Document

@pytest.fixture
def parser():
     return SerperResponseParser()

@pytest.fixture
def web_manager():
     return SerperApiSearchEngine(api_key='test_key')

@pytest.fixture
def web_service(web_manager: SerperApiSearchEngine, parser: SerperResponseParser):
    return WebService(web_manager=web_manager, parser=parser)

def test_provide_documents(web_service: WebService):
    mocked_search_results = {"result": "value"}
    mocked_documents = [Document(data='Test')]
    mocked_query = 'Current date'

    with patch.object(web_service.web_manager,'search_web', return_value=mocked_search_results) as mock_search_web, \
         patch.object(web_service.parser,'parse', return_value=mocked_documents) as mock_parse:
            result = web_service.provide_documents(mocked_query)

    mock_search_web.assert_called_once_with(mocked_query)
    mock_parse.assert_called_once_with(mocked_search_results)
    assert result == mocked_documents
        