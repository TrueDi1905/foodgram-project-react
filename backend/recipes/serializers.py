from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.serializers import CustomUserSerializer
from .models import Tag, Ingredient, Recipe, FavoriteRecipe, User, IngredientAmount, ShoppingCart


from rest_framework import serializers


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


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


class IngredientAmountRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(many=True,
        queryset=Tag.objects.all()
    )
    ingredients = IngredientAmountRecipeSerializer(many=True)
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
        return FavoriteRecipe.objects.filter(user=self.context['request'].user, recipe=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        return ShoppingCart.objects.filter(user=self.context['request'].user, recipes_shop=obj.id).exists()

    def validate(self, data):
        if data['cooking_time'] <= 0:
            raise serializers.ValidationError('Нереально так быстро приготовить')
        return data

    def create(self, validated_data):
        print(validated_data)
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        print(ingredients)
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            print(ingredient)
            current_ingredient = Ingredient.objects.get(id=ingredient['id'].id)
            IngredientAmount.objects.create(
                ingredients=current_ingredient, recipes=recipe, amount=ingredient['amount'])
        return recipe


class ShortRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteRecipeSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if FavoriteRecipe.objects.filter(user=data['user'], recipe=data['recipe']).exists():
            raise serializers.ValidationError('Вы уже добаили рецепт в избранное!')
        return data

    class Meta:
        fields = '__all__'
        model = FavoriteRecipe

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
