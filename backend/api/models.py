from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Version(models.Model):
    name = models.CharField(max_length=100, unique=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='mod_version')
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='mod_categories')
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class FilmCard(models.Model):
    DISPLAY_CHOICES = [
        ('on_display', "Em Cartaz"),
        ('shortly', "Em Breve")
    ]

    AGE_CHOICES = [
        ('livre', "Livre"),
        ('10', "10 Anos"),
        ('12', "12 Anos"),
        ('14', "14 Anos"),
        ('16', "16 Anos"),
        ('18', "18 Anos")
    ]

    name = models.CharField(max_length=200, unique=True)
    category = models.ManyToManyField(Category, related_name='films')
    description = models.TextField()
    version = models.ManyToManyField(Version, related_name='ver_films')
    duration = models.PositiveIntegerField()
    age_rating = models.CharField(choices=AGE_CHOICES, default='livre')
    display = models.CharField(choices=DISPLAY_CHOICES, default='on_display')
    thumb_image = models.FileField(upload_to='thumbs/')
    ticket_url = models.URLField()
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='mod_films')
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Session(models.Model):
    WEEK_CHOICES = [
        ('monday', "Segunda"),
        ('tuesday', "Terça"),
        ('wednesday', "Quarta"),
        ('thursday', "Quinta"),
        ('friday', "Sexta"),
        ('saturday', "Sábado"),
        ('sunday', "Domingo")
    ]

    name = models.CharField(max_length=100, unique=True)
    # time = models.TimeField()
    days_list = models.JSONField(default=list)
    film = models.OneToOneField(FilmCard, on_delete=models.CASCADE, related_name='session_film')
    room = models.CharField(max_length=100)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='modified_sessions')
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
