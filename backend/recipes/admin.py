from django.contrib import admin

from .models import Ingredients


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


admin.site.register(Ingredients, IngredientsAdmin)
