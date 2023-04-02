import logging
import os
from math import ceil
from typing import Optional

from django.shortcuts import redirect, render
from elasticsearch.exceptions import NotFoundError
from elasticsearch_dsl.query import MatchAll, MultiMatch

from main.documents import PypiPackageDocument
from main.main_job import main_job
from main.utils import get_page_number

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

PAGINATE_BY = int(os.environ.get("PAGINATE_BY", 10))


def index(request):
    search_value = request.GET.get("q")
    page_num = request.GET.get("page", 1)
    page_num = get_page_number(page_num)

    packages, p_count = get_paginated_data_from_elastic(search_value, page_num)
    total_pages_num = ceil(p_count / PAGINATE_BY)
    previous_page = max(1, page_num-1)
    next_page = min(page_num + 1, total_pages_num)

    context = {
        "packages": packages,
        "previous_page": previous_page,
        "current_page": page_num,
        "next_page": next_page,
        "total_pages_num": total_pages_num
    }
    return render(request, "main/index.html", context)


def get_paginated_data_from_elastic(search_value: Optional[str], page_number: int):
    if search_value:
        match_query = MultiMatch(
            query=search_value,
            fields=["description", "title", "version", "author_name", "author_email"],
        )
    else:
        match_query = MatchAll()

    start = (page_number-1) * PAGINATE_BY
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
