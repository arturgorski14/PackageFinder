import logging
from django.http import HttpResponse
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch
from django.core.paginator import Paginator

from .models import PypiPackage
from .documents import PypiPackageDocument
from django.template import loader
from django.shortcuts import render

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def index(request):
    search = request.GET.get('q')
    if search:
        mm = MultiMatch(query=search, fields=["description", "title"])
        packages = Search().query(mm)
        packages_count = packages.count()
    else:
        packages = []
        packages_count = 0

    context = {
        "len_packages": packages_count,
        "packages": packages,
        "q_found": search,
    }
    # return render(request, "main/index.html", context)
    return render(request, "main/index.html", context)
