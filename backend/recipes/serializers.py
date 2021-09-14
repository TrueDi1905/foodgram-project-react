from rest_framework import serializers
from .models import Tags, Ingredients, Recipes


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = ('id', 'name', 'color', 'slug')


class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipes
        fields = ('id', 'tags', 'name', 'text', 'ingredients', 'cooking_time')
