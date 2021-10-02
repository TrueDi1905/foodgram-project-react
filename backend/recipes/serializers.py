from rest_framework import serializers

from users.serializers import CustomUserSerializer
from .models import Tags, Ingredients, Recipes, FavoriteRecipes, User, IngredientsAmount, ShoppingCart


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = ('id', 'name', 'color', 'slug')


class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit')


class IngredientsAmountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()
    measurement_unit = serializers.ReadOnlyField()
    amount = serializers.StringRelatedField(many=True)

    class Meta:
        model = IngredientsAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class UserRecipesSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True)
    ingredients = IngredientsAmountSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipes
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited', 'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time')
        depth = 1

    def get_is_favorited(self, obj):
        if FavoriteRecipes.objects.filter(user=self.context['request'].user, recipe=obj.id).exists():
            return 'true'
        return 'false'

    def get_is_in_shopping_cart(self, obj):
        if ShoppingCart.objects.filter(user=self.context['request'].user, recipes_shop=obj.id).exists():
            return 'true'
        return 'false'


class CreateRecipeSerializer(serializers.ModelSerializer):
    author = UserRecipesSerializer(read_only=True)

    class Meta:
        model = Recipes
        fields = '__all__'


class ShortRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteRecipesSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if FavoriteRecipes.objects.filter(user=data['user'], recipe=data['recipe']).exists():
            raise serializers.ValidationError('Вы уже добаили рецепт в избранное!')
        return data

    class Meta:
        fields = '__all__'
        model = FavoriteRecipes

    def to_representation(self, instance):
        serializer = ShortRecipeSerializer(instance.recipe)
        return serializer.data


class ShoppingSerializers(serializers.ModelSerializer):

    def validate(self, data):
        if ShoppingCart.objects.filter(user=data['user'], recipes_shop=data['recipes_shop']).exists():
            raise serializers.ValidationError('Вы уже добавили рецепт в список покупок!')
        return data

    class Meta:
        fields = '__all__'
        model = ShoppingCart

    def to_representation(self, instance):
        serializer = ShortRecipeSerializer(instance.recipes_shop)
        return serializer.data

