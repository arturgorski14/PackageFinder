import pytest

from main.pypi_scrapper import PypiScrapper
from main.utils import create_soup


@pytest.mark.parametrize(
    "url, expected_author",
    [
        (
            "https://pypi.org/project/usu-apex/",
            "AJ Burns aj501173@gmail.com",
        ),
        (
            "https://pypi.org/project/torch-scatter-carate/",
            "Matthias Fey julian.kleber@sail.black",
        ),
        (
            "https://pypi.org/project/random-header-generator/",
            "miltos_90",
        ),
        (
            "https://pypi.org/project/django-admin-site-search/",
            "Ahmed Al-Jawahiry ahmedaljawahiry@gmail.com",
        ),
        pytest.param(
            "https://pypi.org/project/terraform-backend-s3-bucket/",
            "Stefan Freitag stefan.freitag@udo.edu",
            marks=pytest.mark.xfail(reason="Missing <a> tag for email"),
        ),
    ],
)
def test_get_author(url, expected_author):
    soup = create_soup(url)
    name, email = PypiScrapper.find_author(soup)
    assert name, email == expected_author


@pytest.mark.parametrize(
    "project_url, maintainer_url",
    [
        (
            "https://pypi.org/project/usu-apex/",
            "https://pypi.org/user/broboy763/",
        ),
        (
            "https://pypi.org/project/synthesizers/",
            "https://pypi.org/user/petersk/",
        ),
        (
            "https://pypi.org/project/mangadex-dl/",
            "https://pypi.org/user/john-erinjery/",
         )
    ],
)
def test_get_maintainer_userpage(project_url, maintainer_url):
    soup = create_soup(project_url)
    href = PypiScrapper.find_maintainer_userpage(soup)
    assert href == maintainer_url


@pytest.mark.parametrize(
    "url, expected_maintainer",
    [
        ("https://pypi.org/user/broboy763/", "AJ Burns"),
        ("https://pypi.org/user/MQSchleich/", "Manuel"),
        ("https://pypi.org/user/miltos_90/", "Miltos K"),
        ("https://pypi.org/user/bsimpson888/", ""),
        # ("https://pypi.org/user/tinom9/", "Tino Martínez Molina")
    ]
)
def test_get_maintainer(
    url, expected_maintainer,
):
    soup = create_soup(url)
    maintainer = PypiScrapper.find_maintainer(soup)
    assert maintainer == expected_maintainer


@pytest.mark.parametrize(
    "url, expected_description",
    [
        (
            "https://pypi.org/project/usu-apex/",
            "The Aggie Python Engineering eXecution",
        ),
        ("https://pypi.org/project/grandfather/", "WIP"),
    ],
)
def test_get_package_description(url, expected_description):
    soup = create_soup(url)
    description = PypiScrapper.find_description(soup)
    assert description == expected_description


@pytest.mark.parametrize(
    "url, expected_title",
    [
        ("https://pypi.org/project/pyplotbrookings/", "pyplotbrookings"),
    ],
)
def test_get_package_title(url, expected_title):
    soup = create_soup(url)
    title, _ = PypiScrapper.find_title_and_version(soup)
    assert title == expected_title


@pytest.mark.parametrize(
    "url, expected_version",
    [
        ("https://pypi.org/project/AnumbyRobotSJ/", "2.4.6"),
        ("https://pypi.org/project/modbus-wrapper/", "1.0.1"),
        ("https://pypi.org/project/nlp-toolbox/", "0.0.3"),
        ("https://pypi.org/project/address-ping-system/", "0.3.1"),
    ],
)
def test_get_current_version(url, expected_version):
    soup = create_soup(url)
    _, version = PypiScrapper.find_title_and_version(soup)
    assert version == expected_version
