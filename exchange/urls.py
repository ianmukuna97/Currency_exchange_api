from django.urls import path
from . import views

urlpatterns = [
    path("rates/", views.get_rates, name="rates"),
    path("convert/", views.convert_currency, name="convert"),
    path("history/", views.get_historical, name="history"),
]