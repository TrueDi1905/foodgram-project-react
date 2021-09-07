from django.db import models
from django.contrib.auth import get_user_model
from colorfield.fields import ColorField

User = get_user_model()


class Ingredients(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    measurement_unit = models.CharField(max_length=6, verbose_name="Единицы измерения")

    def __str__(self):
        return self.name


class Tags(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    color = ColorField(default='#FF0000')
    slug = models.fields.SlugField(unique=True, verbose_name="Уникальный адрес")


class Recipes(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="recipes", verbose_name='Автор')
    name = models.CharField(max_length=50, verbose_name="Название")
    image = models.ImageField(upload_to='frontend/image')
    text = models.TextField(verbose_name="Описание")
    ingredients = models.ManyToManyField(Ingredients)
    tags = models.ManyToManyField(Tags)
    cooking_time = models.PositiveSmallIntegerField(verbose_name="Время приготовления в минутах")
