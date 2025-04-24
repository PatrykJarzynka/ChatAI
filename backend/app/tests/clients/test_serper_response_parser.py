import pytest
from clients.serper_response_parser import SerperResponseParser
from llama_index.core import Document

@pytest.fixture
def response_parser():
    return SerperResponseParser()

def test_parse_answer_box_included(response_parser: SerperResponseParser):
    mocked_data = {
        "answerBox": {
            "link": "Test link",
            "snippet": "Test answer",
        },
        "organic": [
            {
                "title": "What Is Today's Date? - Inch Calculator",
                "link": "https://www.inchcalculator.com/what-is-todays-date/",
                "snippet": "Today, April 24th , is day 114 of 365 total days in 2025. What is Today's Date in Numbers? Today's date in numbers is: MM- ...",
                "position": 1
            }
        ]
    }

    expected_result = [Document(text=mocked_data['answerBox']["snippet"], metadata={"url": mocked_data['answerBox']["link"]})]

    result = response_parser.parse(mocked_data)

    assert expected_result[0].metadata == result[0].metadata
    assert expected_result[0].text == result[0].text


def test_parse_answer_box_excluded(response_parser: SerperResponseParser):
    mocked_data = {
        "organic": [
            {
                "title": "What Is Today's Date? - Inch Calculator",
                "link": "https://www.inchcalculator.com/what-is-todays-date/",
                "snippet": "Today, April 24th , is day 114 of 365 total days in 2025. What is Today's Date in Numbers? Today's date in numbers is: MM- ...",
                "position": 1
            }
        ]
    }

    expected_result = [Document(text=mocked_data["organic"][0]["snippet"], metadata={"url": mocked_data["organic"][0]["link"]})]

    result = response_parser.parse(mocked_data)

    assert expected_result[0].metadata == result[0].metadata
    assert expected_result[0].text == result[0].text