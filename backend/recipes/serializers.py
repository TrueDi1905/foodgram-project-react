from rest_framework import serializers
from .models import Tags, Ingredients, Recipes, FavoriteRecipes, User
from rest_framework.validators import UniqueTogetherValidator

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = ('id', 'name', 'color', 'slug')


class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Recipes
        fields = ('id', 'author', 'tags', 'name', 'text', 'ingredients', 'cooking_time')
        depth = 1


class FavoriteRecipesSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    recipe = serializers.StringRelatedField()

    def validate(self, attrs):
        user = User.objects.get(id=self.context['request'].user.id)
        recipe = Recipes.objects.get(
            id=self.context['view'].kwargs.get('pk')
        )
        if FavoriteRecipes.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError("Данный рецепт уже есть в 'Избранном!'")
        else:
            return attrs

    class Meta:
        fields = ('user', 'recipe')
        model = FavoriteRecipes
