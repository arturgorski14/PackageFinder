import logging
import requests
from bs4 import BeautifulSoup

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def get_response_content(url) -> bytes:
    response = requests.get(url)
    if response.status_code != 200:
        log.warning(f"Received {response.status_code=} for url {url}")
        return bytes()
    return response.content


def create_soup(url: str) -> BeautifulSoup:
    response_data = get_response_content(url)
    return BeautifulSoup(response_data, "xml")
