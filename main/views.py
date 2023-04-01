import logging

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch
from django.shortcuts import render

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def index(request):
    search_value = request.GET.get('q')
    if search_value:
        packages, packages_count = get_data_from_elastic(search_value)
    else:
        packages = []
        packages_count = 0

    context = {
        "len_packages": packages_count,
        "packages": packages,
        "q_found": search_value,
    }
    # return render(request, "main/index.html", context)
    return render(request, "main/index.html", context)


def get_data_from_elastic(query):
    mm = MultiMatch(query=query, fields=["description", "title"])
    packages = Search(using="packages").query(mm)
    packages_count = packages.count()
    return packages, packages_count
