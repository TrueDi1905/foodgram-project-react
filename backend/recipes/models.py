from django.db import models
from django.contrib.auth import get_user_model
from colorfield.fields import ColorField

User = get_user_model()


class Ingredients(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    measurement_unit = models.CharField(max_length=6, verbose_name="Единицы измерения")

    class Meta:
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return self.name


class Tags(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    color = ColorField(default='#FF0000', verbose_name="Цвет в HEX")
    slug = models.fields.SlugField(unique=True, max_length=200,
                                   verbose_name="Уникальный адрес")

    class Meta:
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Recipes(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="recipes", verbose_name='Автор')
    name = models.CharField(max_length=50, verbose_name="Название")
    image = models.ImageField(upload_to='image')
    text = models.TextField(verbose_name="Описание")
    ingredients = models.ManyToManyField(Ingredients, through='IngredientsAmount')
    tags = models.ManyToManyField('Tags')
    cooking_time = models.PositiveSmallIntegerField(verbose_name="Время приготовления в минутах")

    class Meta:
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return self.name


class IngredientsAmount(models.Model):
    ingredients = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    recipes = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(verbose_name='Кол-во')


class FavoriteRecipes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="user", verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
