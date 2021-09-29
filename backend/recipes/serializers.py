from rest_framework import serializers
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
    author = UserRecipesSerializer(read_only=True)
    tags = serializers.StringRelatedField(many=True)
    ingredients = IngredientsAmountSerializer(many=True)

    class Meta:
        model = Recipes
        fields = '__all__'
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



    class Meta:
        fields = '__all__'
        model = FavoriteRecipes


class ShoppingSerializers(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    recipes_shop = serializers.StringRelatedField()

    def validate(self, attrs):
        user = User.objects.get(id=self.context['request'].user.id)
        recipe = Recipes.objects.get(
            id=self.context['view'].kwargs.get('pk')
        )
        if ShoppingCart.objects.filter(user=user, recipes_shop=recipe).exists():
            raise serializers.ValidationError("Данный рецепт уже есть в в списке покупок")
        else:
            return attrs

    def to_representation(self, instance):
        recipes = ShortRecipeSerializer(instance.recipes_shop)
        return recipes.data

    class Meta:
        fields = '__all__'
        model = ShoppingCart
