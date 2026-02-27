from django.contrib import admin
from .models import CategoryType, Category, FilmGenre, FilmCard, Session

admin.site.register(CategoryType)
admin.site.register(Category)
admin.site.register(FilmGenre)
admin.site.register(FilmCard)
admin.site.register(Session)
