from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('add/', views.create_post_view, name='create_post'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
]