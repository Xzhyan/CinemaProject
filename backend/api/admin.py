from django.contrib import admin
from .models import Session, Category, Version, FilmCard

admin.site.register(Session)
admin.site.register(Category)
admin.site.register(Version)
admin.site.register(FilmCard)
