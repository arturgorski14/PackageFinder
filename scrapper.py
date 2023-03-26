import logging
from typing import Tuple

from bs4 import BeautifulSoup, Tag, NavigableString

log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)


class Scrapper:
    @classmethod
    def find_author(cls, soup: BeautifulSoup) -> Tuple[str, str]:
        author = soup.find("strong", string="Author:")
        data = author.parent.contents[-1]
        name = data.get_text(strip=True)
        if isinstance(data, NavigableString):
            email = ""
        else:
            email = data.get("href").replace("mailto:", "")
        return name, email

    @classmethod
    def find_description(cls, soup: BeautifulSoup) -> str:
        tag = soup.find("p", class_="package-description__summary")
        if not tag.contents:
            cls.__message(tag)
            return ""
        return tag.contents[0].string

    @classmethod
    def find_maintainer(cls, soup: BeautifulSoup) -> Tuple[str, str, str]:
        """
        Returns: data of the author such as name, surname and email.
        If unable to scrap then returns values as empty string
        """
        tag = soup.find("h1", class_="author-profile__name")
        name = surname = email = ""
        if not tag.contents:
            cls.__message(tag)
        else:
            data = tag.contents[0].get_text(strip=True).split(" ")
            data += [""] * (3 - len(data))  # fill up to 3 values
            (
                name,
                surname,
                email,
                *_,
            ) = data  # get rid of possiblity of having more than 3 items
        return name, surname, email

    @classmethod
    def find_title_and_version(cls, soup: BeautifulSoup) -> Tuple[str, str]:
        tag = soup.find("h1", class_="package-header__name")
        if not tag.contents:
            cls.__message(tag)
            return "", ""
        title, version = tag.contents[0].get_text(strip=True).split(" ")
        return title, version

    @staticmethod
    def __message(tag: Tag):
        log.warning(f"Cannot find attribute in {tag=}")
