import logging

from django.shortcuts import redirect, render
from elasticsearch.exceptions import NotFoundError
from elasticsearch_dsl.query import MatchAll, MultiMatch
from django.core.paginator import Paginator

from main.documents import PypiPackageDocument
from main.main_job import main_job

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def index(request):
    search_value = request.GET.get("q")
    packages = get_data_from_elastic(search_value)

    context = {
        "packages": packages,
    }
    return render(request, "main/index.html", context)


def get_data_from_elastic(search_value):
    if search_value:
        match_query = MultiMatch(
            query=search_value,
            fields=["description", "title", "version", "author_name", "author_email"],
        )
    else:
        match_query = MatchAll()
    packages_query = PypiPackageDocument.search()[:100].query(match_query)

    try:
        _ = packages_query.count()
    except NotFoundError:
        return []
    else:
        return packages_query


def populate_index_on_demand(request):
    main_job()
    return redirect("/")
