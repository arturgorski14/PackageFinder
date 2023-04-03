import logging

from main.models import PypiPackage
from main.pypi_scrapper import PypiScrapper
from main.utils import create_soup

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def main_job():
    url = "https://pypi.org/rss/packages.xml"
    soup = create_soup(url)

    all_package_links = soup.find_all("link")
    for tag in list(set(all_package_links)):
        package_url = tag.string
        log.info(f"Processing {package_url=}")
        if package_url == "https://pypi.org/":
            log.info("Skip")
            continue

        package_soup = create_soup(package_url)
        author_name, author_email = PypiScrapper.find_author(package_soup)
        title, version = PypiScrapper.find_title_and_version(package_soup)
        description = PypiScrapper.find_description(package_soup)
        maintainer = PypiScrapper.find_maintainer(
            create_soup(PypiScrapper.find_maintainer_userpage(package_soup))
        )

        save_data_to_elastic(
            author_name=author_name,
            author_email=author_email,
            title=title,
            version=version,
            description=description,
            maintainer=maintainer,
        )
    log.info("main_job has finished")


def save_data_to_elastic(**kwargs):
    log.info("Saving to elastic")
    package = PypiPackage(**kwargs)
    package.save()


if __name__ == "__main__":
    main_job()
