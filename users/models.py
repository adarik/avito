from django.db import models


class Location(models.Model):
    name = models.TextField(max_length=300)
    lat = models.DecimalField(max_digits=8, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=8, decimal_places=6, null=True)

    class Meta:
        verbose_name = 'Местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class User(models.Model):
    ROLES = [
        ('member', "Пользователь"),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    ]

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=25, null=True, blank=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=9, choices=ROLES, default='member')
    age = models.PositiveIntegerField()
    location = models.ManyToManyField(Location)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username
