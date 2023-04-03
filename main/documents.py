from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from main.models import PypiPackage


@registry.register_document
class PypiPackageDocument(Document):
    class Index:
        name = "packages"
        settings = {"number_of_shards": 1, "number_of_replicas": 1}

    class Django:
        model = PypiPackage

        fields = [
            "author_email",
            "author_name",
            "description",
            "title",
            "version",
            "maintainer",
        ]
