from http import HTTPStatus

import pytest
from django.test import Client
from elasticsearch_dsl.connections import connections

connections.create_connection(
    hosts=["localhost", "elasticsearch:9200"]
)  # do testów elastica - zmockowac connections


class TestMainIndexView:
    client = Client()

    @pytest.mark.parametrize(
        "pattern",
        [
            "",
            "/",
        ],
    )
    def test_render_default_page(self, pattern):
        response = self.client.get(pattern)
        assert response.status_code == HTTPStatus.OK
        assert response.context["packages"] == []
        assert "No packages found." in str(response.content)

    @pytest.mark.parametrize(
        "param",
        [
            "?invalid_param=",
            "?invalid_param=value",
            "?q=",
        ],
    )
    def test_invalid_query_search_parameter_should_be_ommited(self, param):
        param = "?param"
        response = self.client.get(param)
        assert response.status_code == HTTPStatus.OK
        assert response.context["packages"] == []
        assert "No packages found." in str(response.content)
