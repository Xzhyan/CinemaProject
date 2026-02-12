from rest_framework import serializers
from .models import Category, FilmCard

class FilmCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilmCard
        fields = '__all__'
