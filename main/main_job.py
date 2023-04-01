import logging

# from main.documents import PypiPackageDocument
from main.models import PypiPackage
from main.utils import create_soup
from main.pypi_scrapper import PypiScrapper

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def main_job():
    log.info("MAIN JOB STARTS")
    url = "https://pypi.org/rss/packages.xml"
    soup = create_soup(url)

    all_package_links = soup.find_all("link")
    log.debug(all_package_links)
    for tag in all_package_links[1:]:  # first is redundant
        package_url = tag.string
        log.debug(package_url)

        package_soup = create_soup(package_url)
        # author = PypiScrapper.find_author(package_soup)
        title, version = PypiScrapper.find_title_and_version(package_soup)
        description = PypiScrapper.find_description(package_soup)
        # maintainer = PypiScrapper.find_maintainer(
        #     create_soup(PypiScrapper.find_maintainer_userpage(package_soup))
        # )
        #
        # if description:
        #     save_data_to_elastic(description)

        # print(f"{author=}\n{title=}\n{version=}\n{description=}\n{maintainer=}\n")
        save_data_to_elastic(title=title, version=version, description=description)
    log.info("MAIN JOB ENDED")


def save_data_to_elastic(**kwargs):
    log.info("Saving to elastic")
    package = PypiPackage(**kwargs)
    package.save()


if __name__ == "__main__":
    main_job()
