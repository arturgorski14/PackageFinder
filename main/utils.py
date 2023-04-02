import logging

import requests
from bs4 import BeautifulSoup

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def get_response_content(url: str) -> bytes:
    response = requests.get(url)
    if response.status_code != 200:
        log.warning(f"Received {response.status_code=} for url {url}")
        return bytes()
    return response.content


def create_soup(url: str) -> BeautifulSoup:
    """
    Create BeautifulSoup object for scrapper
    xml option can process .html also
    """
    response_data = get_response_content(url)
    return BeautifulSoup(response_data, "xml")


def get_page_number(number) -> int:
    """
    Get page number for pagination.
    Django paginator doesn't support Elasticsearch Query.
    Function allows number > page_number
    """
    default_page_number = 1
    try:
        if isinstance(number, float) and not number.is_integer():
            raise ValueError
        number = int(number)
    except (TypeError, ValueError):
        return default_page_number

    return max(number, default_page_number)
