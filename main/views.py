from django.shortcuts import redirect, render

from PackageFinder.settings import PAGINATE_BY
from main.main_job import main_job
from django_elasticsearch_dsl_drf.pagination import Paginator

from main.utils import get_paginated_data_from_elastic


def index(request):
    search_value = request.GET.get("q")
    page_num = request.GET.get("page", 1)

    packages = get_paginated_data_from_elastic(search_value, int(page_num))

    if not packages:
        page_obj = []
    else:
        paginator = Paginator(packages, PAGINATE_BY)
        page_obj = paginator.get_page(page_num)

    context = {
        "page_obj": page_obj,
    }
    return render(request, "main/index.html", context)


def populate_index_on_demand(request):
    main_job()
    return redirect("/")
