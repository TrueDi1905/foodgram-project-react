from django.contrib import admin

from .models import (FavoriteRecipe, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug', 'id')
    search_fields = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name',)
    search_fields = ('name',)


class AmountIngAdmin(admin.ModelAdmin):
    list_display = ('recipes', 'amount',)


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('recipes_shop', 'user')


admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientAmount, AmountIngAdmin)
admin.site.register(FavoriteRecipe)
