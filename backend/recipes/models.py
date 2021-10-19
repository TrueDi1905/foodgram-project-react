from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    measurement_unit = models.CharField(
        max_length=200, verbose_name="Единицы измерения"
    )

    class Meta:
        verbose_name_plural = "Ингридиенты"
        verbose_name = "Ингрдиент"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    color = ColorField(default='#FF0000', verbose_name="Цвет в HEX")
    slug = models.fields.SlugField(unique=True, max_length=200,
                                   verbose_name="Уникальный адрес")

    class Meta:
        verbose_name_plural = "Теги"
        verbose_name = "Тег"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="recipes", verbose_name="Автор")
    name = models.CharField(max_length=50, verbose_name="Название")
    image = models.ImageField()
    text = models.TextField(verbose_name="Описание")
    ingredients = models.ManyToManyField(
        Ingredient, through="IngredientAmount"
    )
    tags = models.ManyToManyField("Tag")
    cooking_time = models.CharField(
        verbose_name="Время приготовления в минутах"
    )

    class Meta:
        verbose_name_plural = "Рецепты"
        verbose_name = "Рецепт"

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    ingredients = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name="ingredient_amount"
    )
    recipes = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="ingredient_amount")
    amount = models.IntegerField(verbose_name="Кол-во")

    class Meta:
        verbose_name_plural = "Кол-во ингридиентов"
        verbose_name = "Кол-во ингридиента"
        constraints = [
            models.UniqueConstraint(
                fields=['recipes', 'ingredients'],
                name='unique_ingredients',
            ),
        ]


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="favorite_user",
                             verbose_name="Пользователь"
                             )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="favorite_recipe")

    class Meta:
        verbose_name_plural = "Список избранного"
        verbose_name = "Список в избранного"
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite_recipe',
            ),
        ]


class ShoppingCart(models.Model):
    recipes_shop = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                                     related_name="shop_recipe"
                                     )
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name="Пользователь"
                             )

    class Meta:
        verbose_name_plural = "Список покупок"
        verbose_name = "Список в покупок"
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipes_shop'],
                name='unique_shop_cart',
            ),
        ]
