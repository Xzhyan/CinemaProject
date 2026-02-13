from django.urls import path
from . import views

urlpatterns = [
    path('control-panel/', views.control_panel, name='control-panel'),
    path('users/', views.users, name='users'),
    path('films/', views.films, name='films'),
    path('categories/', views.categories, name='categories')
]
