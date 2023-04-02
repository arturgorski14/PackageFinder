from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("fill", views.populate_index_on_demand, name="fill"),
]
