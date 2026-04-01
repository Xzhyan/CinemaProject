from django.urls import path
from . import views

urlpatterns = [
    path('films/', views.films),
    path('sessions/', views.sessions),
    path('promotions/', views.promotions),
]
