from django.urls import path
from . import views

urlpatterns = [
    path('control-panel/', views.control_panel, name='control-panel'),
    path('users/', views.users, name='users'),
    path('films/', views.films, name='films'),
    path('film-edit/<int:id>/', views.film_edit, name='film-edit'),
    path('categories/', views.categories, name='categories'),
    path('category-edit/<int:id>/', views.category_edit, name='category-edit')
]
