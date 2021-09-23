from rest_framework import serializers
from .models import Tags, Ingredients, Recipes, FavoriteRecipes, User, IngredientsAmount


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
    tags = serializers.StringRelatedField(many=True)
    ingredients = serializers.StringRelatedField(many=True)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
    class Meta:
        model = Recipes
        fields = ('id', 'tags', 'name', 'text', 'ingredients', 'cooking_time', 'author',)
        depth = 1


class ShortRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time')


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

    def to_representation(self, instance):
        recipes = ShortRecipeSerializer(instance.recipe)
        return recipes.data

    class Meta:
        fields = '__all__'
        model = FavoriteRecipes

