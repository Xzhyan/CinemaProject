from rest_framework import serializers
from .models import CategoryType, Category, FilmGenre, FilmCard, Session
from collections import defaultdict


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class FilmGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilmGenre
        fields = ['id', 'name']


class FilmCardSerializer(serializers.ModelSerializer):
    film_genre = FilmGenreSerializer(many=True)

    display_label = serializers.CharField(
        source='get_display_display',
        read_only=True
    )

    class Meta:
        model = FilmCard
        fields = ['id', 'name', 'display_label', 'film_genre', 'description', 'duration', 'director', 'movie_cast', 'age_rating', 'thumb_image', 'banner_image']

class SessionSerializer(serializers.ModelSerializer):
    catg_grouped = serializers.SerializerMethodField()

    week_day = serializers.CharField(
        source='get_week_day_display',
        read_only=True
    )

    class Meta:
        model = Session
        fields = ['id', 'name', 'film', 'catg_grouped', 'week_day', 'date', 'room', 'ticket_url']

    def get_catg_grouped(self, obj):
        grouped = defaultdict(list)

        for catg in obj.categories.all():
            key = catg.category_type.name
            grouped[key].append(CategorySerializer(catg).data)

        return grouped