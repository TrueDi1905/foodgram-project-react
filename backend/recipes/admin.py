from django.contrib import admin

from .models import Ingredients, Tags, Recipes, IngredientsAmount


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name',)


class RecipesAdmin(admin.ModelAdmin):
    list_display = ('author', 'name')
    search_fields = ('name',)


class AmountIngAdmin(admin.ModelAdmin):
    list_display = ('recipes', 'amount',)


admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Recipes, RecipesAdmin)
admin.site.register(IngredientsAmount, AmountIngAdmin)
