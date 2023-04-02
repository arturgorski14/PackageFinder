from main.models import PypiPackage
from main.pypi_scrapper import PypiScrapper
from main.utils import create_soup


def main_job():
    print("MAIN JOB STARTS")
    url = "https://pypi.org/rss/packages.xml"
    soup = create_soup(url)

    all_package_links = soup.find_all("link")
    print(all_package_links)
    for tag in list(set(all_package_links))[1:]:  # first is redundant
        package_url = tag.string
        print(package_url)

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
        save_data_to_elastic(
            title=title,
            version=version,
            description=description,
        )
    print("MAIN JOB ENDED")


def save_data_to_elastic(**kwargs):
    print("Saving to elastic")
    package = PypiPackage(**kwargs)
    package.save()


if __name__ == "__main__":
    main_job()
