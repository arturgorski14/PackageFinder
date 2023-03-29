from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from main.models import Package


@registry.register_document
class PackageDocument(Document):

    class Index:
        name = "packages"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Package

        fields = [
            "description",
        ]
