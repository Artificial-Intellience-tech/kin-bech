from django.urls import path
from . import views

app_name = "market"

urlpatterns = [
    path("", views.marketplace_list, name="marketplace"),
    path("sell/", views.create_sell_request, name="create_sell_request"),
    path("sell/<int:pk>/delete/", views.delete_sell_request, name="delete_sell_request"),
]