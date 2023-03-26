import pytest

from scrapper import Scrapper
from utils import create_soup


@pytest.mark.parametrize(
    "url, expected_author, expected_email",
    [
        (
            "https://pypi.org/project/usu-apex/",
            "AJ Burns",
            "aj501173@gmail.com",
        ),
        (
            "https://pypi.org/project/torch-scatter-carate/",
            "Matthias Fey",
            "julian.kleber@sail.black",
        ),
        (
            "https://pypi.org/project/random-header-generator/",
            "miltos_90",
            "",
        ),
        (
            "https://pypi.org/project/django-admin-site-search/",
            "Ahmed Al-Jawahiry",
            "ahmedaljawahiry@gmail.com",
        ),
        pytest.param(
            "https://pypi.org/project/terraform-backend-s3-bucket/",
            "Stefan Freitag",
            "stefan.freitag@udo.edu",
            marks=pytest.mark.xfail(reason="Missing <a> tag for email"),
        ),
    ],
)
def test_get_author(url, expected_author, expected_email):
    soup = create_soup(url)
    name, email = Scrapper.find_author(soup)
    assert name == expected_author
    assert email == expected_email


@pytest.mark.parametrize(
    "url, expected_name, expected_surname, expected_mail",
    [
        ("https://pypi.org/user/broboy763/", "AJ", "Burns", ""),
        ("https://pypi.org/user/MQSchleich/", "Manuel", "", ""),
        ("https://pypi.org/user/miltos_90/", "Miltos", "K", ""),
    ],
)
def test_get_maintainer(
    url, expected_name, expected_surname, expected_mail
):  # dane osoby utrzymującej pakiet (imię i nazwisko, mail)
    soup = create_soup(url)
    name, surname, email = Scrapper.find_maintainer(soup)
    assert name == expected_name
    assert surname == expected_surname
    assert email == expected_mail


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
    description = Scrapper.find_description(soup)
    assert description == expected_description


@pytest.mark.parametrize(
    "url, expected_title",
    [
        ("https://pypi.org/project/pyplotbrookings/", "pyplotbrookings"),
    ],
)
def test_get_package_title(url, expected_title):
    soup = create_soup(url)
    title, _ = Scrapper.find_title_and_version(soup)
    assert title == expected_title


def test_get_keywords():
    raise NotImplementedError


@pytest.mark.parametrize(
    "url, expected_version",
    [
        ("https://pypi.org/project/AnumbyRobotSJ/", "2.0.0"),
        ("https://pypi.org/project/modbus-wrapper/", "1.0"),
        ("https://pypi.org/project/nlp-toolbox/", "0.0.3"),
        ("https://pypi.org/project/address-ping-system/", "0.3.1"),
    ],
)
def test_get_current_version(url, expected_version):
    soup = create_soup(url)
    _, version = Scrapper.find_title_and_version(soup)
    assert version == expected_version
