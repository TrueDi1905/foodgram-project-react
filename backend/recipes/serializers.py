from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.serializers import CustomUserSerializer
from .fields import Base64ImageField
from .models import (FavoriteRecipe, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag, User)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class UserRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all())
    name = serializers.CharField(read_only=True, source='ingredients.name')
    measurement_unit = serializers.CharField(
        read_only=True, source='ingredients.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )
    ingredients = IngredientRecipeSerializer(
        many=True, source='ingredient_amount')
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'name', 'image', 'text',
                  'cooking_time'
                  )

    def validate(self, data):
        if data['cooking_time'] < 1:
            raise serializers.ValidationError(
                {'name': 'Нереально так быстро приготовить.'})
        if Recipe.objects.filter(name=data['name']) and (
                self.context['request'].method == 'POST'):
            raise serializers.ValidationError(
                'Рецепт с таким именем уже есть!')
        return data

    def validate_ingredients(self, data):
        ingredients = self.initial_data.get('ingredients')
        ingredients_set = set()
        if not ingredients:
            raise serializers.ValidationError(
                'Добавьте хотя бы один ингредиент')
        for ingredient in ingredients:
            if int(ingredient['amount']) < 1:
                raise serializers.ValidationError(
                    'Количество ингредиента не может быть меньше 1.')
            ingredient_id = ingredient.get('id')
            if ingredient_id in ingredients_set:
                raise serializers.ValidationError(
                    'Ингредиент в списке должен быть уникальным.'
                )
            ingredients_set.add(ingredient_id)
        return data

    def validate_tags(self, data):
        tags_set = set()
        if not data:
            raise serializers.ValidationError(
                'Добавьте хотя бы один тэг')
        for tag in data:
            if tag in tags_set:
                raise serializers.ValidationError(
                    'Ингредиент в списке должен быть уникальным.'
                )
            tags_set.add(tag)
        return data

    def ingredient_add(self, ingredients, recipe):
        for ingredient in ingredients:
            current_ingredient = get_object_or_404(
                Ingredient, id=ingredient['id'].id)
            IngredientAmount.objects.get_or_create(
                ingredients=current_ingredient,
                recipes=recipe,
                amount=ingredient['amount'])
        return recipe

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredient_amount')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        recipe = self.ingredient_add(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredient_amount')
        instance.name = validated_data['name']
        instance.text = validated_data['text']
        instance.cooking_time = validated_data['cooking_time']
        instance.tags.set(tags)
        instance.ingredients.clear()
        instance = self.ingredient_add(ingredients, instance)
        instance.save()
        return instance


class RecipeGetSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True)
    ingredients = IngredientRecipeSerializer(
        many=True, source='ingredient_amount')
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time'
                  )

    def get_is_favorited(self, obj):
        return FavoriteRecipe.objects.filter(
            user=self.context['request'].user.id, recipe=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        return ShoppingCart.objects.filter(
            user=self.context['request'].user.id, recipes_shop=obj.id).exists()


class ShortRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteRecipeSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if FavoriteRecipe.objects.filter(
                user=data['user'], recipe=data['recipe']).exists():
            raise serializers.ValidationError(
                'Вы уже добаили рецепт в избранное!')
        return data

    class Meta:
        fields = '__all__'
        model = FavoriteRecipe

    def to_representation(self, instance):
        serializer = ShortRecipeSerializer(instance.recipe)
        return serializer.data


class ShoppingSerializers(serializers.ModelSerializer):

    def validate(self, data):
        if ShoppingCart.objects.filter(
                user=data['user'],
                recipes_shop=data['recipes_shop']).exists():
            raise serializers.ValidationError(
                'Вы уже добавили рецепт в список покупок!')
        return data

    class Meta:
        fields = '__all__'
        model = ShoppingCart

    def to_representation(self, instance):
        serializer = ShortRecipeSerializer(instance.recipes_shop)
        return serializer.data
