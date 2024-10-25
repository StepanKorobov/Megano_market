from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """
    Таблица профиля пользователей
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullName = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.fullName


class Avatar(models.Model):
    """
    Таблица аватара пользователей
    """

    profile = models.OneToOneField(
        Profile, related_name="avatar", on_delete=models.CASCADE
    )
    src = models.ImageField(blank=True, upload_to="profiles/avatars/")
    alt = models.CharField(max_length=120)
