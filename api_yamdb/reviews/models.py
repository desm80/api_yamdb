from django.contrib.auth.models import AbstractUser
from django.db import models


class Category(models.Model):
    pass


class Genre(models.Model):
    pass


class Title(models.Model):
    pass


class Review(models.Model):
    pass


class Comment(models.Model):
    pass


class User(AbstractUser):
    pass

