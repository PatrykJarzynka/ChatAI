import pytest
from utilities.microsoft_public_keys_provider import MicrosoftPublicKeysProvider
from unittest.mock import patch

@pytest.fixture
def microsoft_public_keys_provider():
    return MicrosoftPublicKeysProvider()


def test_get_openid_config(microsoft_public_keys_provider: MicrosoftPublicKeysProvider):

    with patch('request.get') as mock_get:
        microsoft_public_keys_provider.get_openid_config()