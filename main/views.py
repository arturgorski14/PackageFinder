from typing import Optional

from django.shortcuts import redirect, render
from elasticsearch.exceptions import NotFoundError
from elasticsearch_dsl.query import MatchAll, MultiMatch

from PackageFinder.settings import PAGINATE_BY
from main.documents import PypiPackageDocument
from main.main_job import main_job
from django_elasticsearch_dsl_drf.pagination import Paginator


def index(request):
    search_value = request.GET.get("q")
    page_num = request.GET.get("page", 1)

    packages, p_count = get_paginated_data_from_elastic(search_value, int(page_num))

    paginator = Paginator(packages, PAGINATE_BY)
    page_obj = paginator.get_page(page_num)

    context = {
        "page_obj": page_obj,
    }
    return render(request, "main/index.html", context)


def get_paginated_data_from_elastic(
    search_value: Optional[str],
    page_number: int,
):
    if search_value:
        match_query = MultiMatch(
            query=search_value,
            fields=[
                "description",
                "title",
                "version",
                "author_name",
                "author_email",
            ],
        )
    else:
        match_query = MatchAll()

    start = (page_number - 1) * PAGINATE_BY
    end = start + PAGINATE_BY

    packages_query = PypiPackageDocument.search()[start:end].query(match_query)

    try:
        _ = packages_query.count()
    except NotFoundError:
        return [], 0
    else:
        return packages_query, packages_query.count()


def populate_index_on_demand(request):
    main_job()
    return redirect("/")
