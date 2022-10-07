from django.contrib.auth.models import AbstractUser
from django.db import models


class Category(models.Model):
    ...


class Genre(models.Model):
    ...


class Title(models.Model):
    ...


class Review(models.Model):
    ...


class Comment(models.Model):
    ...


class User(AbstractUser):
    ...

