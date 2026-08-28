from django.urls import path
from . import views

app_name = "market"

urlpatterns = [
    path("", views.marketplace_list, name="marketplace"),
    path("create/", views.create_sell_request, name="create_sell_request"),
]