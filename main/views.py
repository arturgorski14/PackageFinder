from django.http import HttpResponse
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch

from .models import PypiPackage
from .documents import PypiPackageDocument
from django.template import loader
from django.shortcuts import render


def index(request):
    q = request.GET.get('q')
    if q:
        print("q exists!")
    else:
        print("q not found")
    query_string = "Payment"
    mm = MultiMatch(query=query_string, fields=["description", "title"])
    packages = Search().query(mm)
    context = {
        "packages": packages
    }
    # return render(request, "main/index.html", context)
    return render(request, "main/index.html", context)
