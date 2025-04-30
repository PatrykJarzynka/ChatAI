import pytest
from utilities.token_extractor import TokenExtractor
from fastapi import HTTPException, status

@pytest.fixture
def get_token_extractor():
    return TokenExtractor()

@pytest.fixture
def header_request():
    class MockRequest:
        def __init__(self):
            self.headers = {"Authorization": 'Bearer XYZ'}

    return MockRequest()

@pytest.fixture
def no_header_request():
    class MockRequest:
        def __init__(self):
            self.headers = {"Authorization": ''}

    return MockRequest()

@pytest.fixture
def wrong_type_request():
    class MockRequest:
        def __init__(self):
            self.headers = {"Authorization": 'XYZ'}

    return MockRequest()

def test_get_token_from_header(get_token_extractor: TokenExtractor, header_request):
    assert get_token_extractor.get_token_from_header(header_request) == 'XYZ', 'Tokens are not the same'

def test_lack_of_token(get_token_extractor: TokenExtractor, no_header_request):
    with pytest.raises(HTTPException) as no_token_exception:
        get_token_extractor.get_token_from_header(no_header_request)

    assert no_token_exception.value.status_code == status.HTTP_401_UNAUTHORIZED, 'Status code should be 401'
    assert no_token_exception.value.detail == 'Authorization header missing', 'Exception message should be equal "Authorization header missing"'

def test_wrong_token_type(get_token_extractor: TokenExtractor, wrong_type_request):
    with pytest.raises(HTTPException) as no_token_exception:
        get_token_extractor.get_token_from_header(wrong_type_request)
        
    assert no_token_exception.value.status_code == status.HTTP_401_UNAUTHORIZED,'Status code should be 401'
    assert no_token_exception.value.detail == 'Invalid token type', 'Exception message should be equal "Invalid token type"'