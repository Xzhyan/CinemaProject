from django.urls import path
from . import views

urlpatterns = [
    # Login and home
    path('login/', views.user_login, name='user-login'),
    path('logout/', views.user_logout, name='user-logout'),
    path('control-panel/', views.control_panel, name='control-panel'),

    # Usuários
    path('users/', views.users, name='users'),
    path('user/edit/<int:id>', views.user_edit, name='user-edit'),

    # Filmes
    path('films/', views.films, name='films'),
    path('film/edit/<int:id>/', views.film_edit, name='film-edit'),

    # Categorias
    path('categories/', views.categories, name='categories'),
    path('category/edit/<int:id>/', views.category_edit, name='category-edit'),

    # Sessões
    path('sessions/', views.sessions, name='sessions'),
    path('sessions/edit/<int:id>', views.session_edit, name='session-edit')
]
