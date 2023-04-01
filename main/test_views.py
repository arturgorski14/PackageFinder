from unittest.mock import Mock

import pytest

from django.test import Client
from http import HTTPStatus

from main.models import PypiPackage


class TestMainIndexView:
    client = Client()

    @pytest.mark.parametrize("pattern", [
        "", "/",
    ])
    def test_render_default_page(self, pattern):
        response = self.client.get(pattern)
        assert response.status_code == HTTPStatus.OK
        assert response.context["packages"] == []
        assert "No packages found." in str(response.content)

    @pytest.mark.parametrize("param", [
        "?invalid_param=",
        "?invalid_param=value",
        "?q=",
    ])
    def test_invalid_query_search_parameter_should_be_ommited(self, param):
        param = "?param"
        response = self.client.get(param)
        assert response.status_code == HTTPStatus.OK
        assert response.context["packages"] == []
        assert "No packages found." in str(response.content)

    @pytest.mark.django_db
    def test_correct_query_search_parameter_should_get_packages(self):
        param = "?q=correct value"
        p1 = PypiPackage(description="correct value", title="some title", version="1.3.0")
        p1.save()
        p2 = PypiPackage(description="xd value", title="xd title", version="0.15")
        p2.save()

        response = self.client.get(param)
        assert response.status_code == HTTPStatus.OK
        assert response.context["packages"] == [p1]
        assert "No packages found." in str(response.content)
