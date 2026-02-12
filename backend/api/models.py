from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class FilmCard(models.Model):
    name = models.CharField(max_length=200)
    categories = models.ManyToManyField(Category, related_name='films', blank=True)
    description = models.TextField()
    duration = models.PositiveIntegerField()
    age_to_watch = models.PositiveIntegerField()
    img_url = models.URLField()
    ticket = models.URLField()

    def __str__(self):
        return self.name
