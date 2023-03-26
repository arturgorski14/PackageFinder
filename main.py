import logging

from utils import create_soup

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def main():
    url = "https://pypi.org/rss/packages.xml"
    soup = create_soup(url)

    all_package_links = soup.find_all("link")
    for tag in all_package_links[1:]:  # first is redundant
        print(tag.string)


if __name__ == "__main__":
    main()
