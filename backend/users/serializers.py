from django.contrib.auth import get_user_model
from djoser.conf import settings
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from recipes.models import Recipe
from users.models import Subscription

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            'username', 'first_name',
            'last_name', 'email', 'is_subscribed')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
        }

    def get_is_subscribed(self, obj):
        if not self.context:
            return True
        user = self.context['request'].user.id
        return Subscription.objects.filter(user=user, follow=obj.id).exists()


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.LOGIN_FIELD,
            settings.USER_ID_FIELD,
            'password', 'last_name', 'first_name', 'username'
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},

        }


class SubscribeRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe


def get_recipes(obj):
    serializer = SubscribeRecipeSerializer(obj, many=True)
    return serializer.data


class SubscribeSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Subscription

    def validate(self, data):
        if data['user'] == data['follow']:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!')
        if Subscription.objects.filter(
                user=data['user'], follow=data['follow']).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого парня!')
        return data

    def to_representation(self, instance):
        follow = CustomUserSerializer(instance.follow).data
        recipes = get_recipes(Recipe.objects.filter(
            author=instance.follow))
        recipe_count = get_recipes_count(instance.follow)
        result = follow
        result['recipes'] = recipes
        result['recipe_count'] = recipe_count
        return result


def get_recipes_count(obj):
    return len(Recipe.objects.filter(author=obj))


class SubscriptionSerializer(serializers.ModelSerializer):
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Subscription

    def to_representation(self, instance):
        follow = CustomUserSerializer(instance.follow).data
        recipes = get_recipes(Recipe.objects.filter(
            author=instance.follow))
        if self.context['request'].query_params.get(
                'recipes_limit'):
            recipes_limit = self.context['request'].query_params.get(
                'recipes_limit')
            recipes = get_recipes(Recipe.objects.filter(
                author=instance.follow)[:int(recipes_limit)])
        recipe_count = get_recipes_count(instance.follow)
        result = follow
        result['recipes'] = recipes
        result['recipe_count'] = recipe_count
        return result
