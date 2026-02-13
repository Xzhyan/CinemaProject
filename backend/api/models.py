from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class FilmCard(models.Model):
    DISPLAY_CHOICES = [
        ('on_display', "Em Cartaz"),
        ('shortly', "Em Breve")
    ]

    name = models.CharField(max_length=200, unique=True)
    category = models.ManyToManyField(Category, related_name='films')
    description = models.TextField()
    duration = models.PositiveIntegerField()
    age_control = models.PositiveIntegerField()
    display = models.CharField(choices=DISPLAY_CHOICES, default='on_display')
    thumb_url = models.URLField()
    ticket_url = models.URLField()

    def __str__(self):
        return self.name
