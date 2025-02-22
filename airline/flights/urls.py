from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('search', views.search, name="search"),
    path('airport/<int:id>', views.airports, name="airport"),
    path('flight/<int:id>', views.flights, name="flight")
]