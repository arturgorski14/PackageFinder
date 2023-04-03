from django.shortcuts import redirect, render

from main.main_job import main_job
from main.utils import get_page_object, get_paginated_data_from_elastic


def index(request):
    search_value = request.GET.get("q")
    page_num = int(request.GET.get("page", 1))

    packages = get_paginated_data_from_elastic(search_value, page_num)
    page_obj = get_page_object(packages, page_num)

    context = {
        "page_obj": page_obj,
    }
    return render(request, "main/index.html", context)


def populate_index_on_demand(request):
    main_job()
    return redirect("/")
