from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('search', views.search),
    path('airport/<int:id>', views.airports),
    path('flight/<int:id>', views.flights)
]