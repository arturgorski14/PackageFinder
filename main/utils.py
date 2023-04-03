import logging
from typing import Optional

import requests
from bs4 import BeautifulSoup
from elasticsearch import NotFoundError
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch, MatchAll

from PackageFinder.settings import PAGINATE_BY
from main.documents import PypiPackageDocument

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


def get_paginated_data_from_elastic(
    search_value: Optional[str],
    page_number: int,
) -> Optional[Search]:
    if search_value:
        match_query = MultiMatch(
            query=search_value,
            fields=[
                "description",
                "title",
                "version",
                "author_name",
                "author_email",
                "maintainer",
            ],
        )
    else:
        match_query = MatchAll()

    start = (page_number - 1) * PAGINATE_BY
    end = start + PAGINATE_BY

    packages_query = PypiPackageDocument.search()[start:end].query(match_query)

    try:
        _ = packages_query.count()
    except NotFoundError:
        return None
    else:
        return packages_query
