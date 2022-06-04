from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import check_birth_date, check_email_domain


class Location(models.Model):
    name = models.TextField(max_length=300)
    lat = models.DecimalField(max_digits=8, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=8, decimal_places=6, null=True)

    class Meta:
        verbose_name = 'Местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class User(AbstractUser):
    MEMBER = 'member'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = [
        (MEMBER, "Пользователь"),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    ]

    role = models.CharField(max_length=9, choices=ROLES, default=MEMBER)
    age = models.PositiveIntegerField(null=True)
    location = models.ManyToManyField(Location)
    birth_date = models.DateField(validators=[check_birth_date], null=True)
    email = models.EmailField(unique=True, validators=[check_email_domain], null=True)

    class Meta:
        ordering = ['username']
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username
