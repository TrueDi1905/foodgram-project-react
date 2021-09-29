from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from djoser.conf import settings
from recipes.models import Recipes
from users.models import Subscriptions

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD, 'last_name', 'first_name', 'email', 'username', 'is_subscribed')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
        }

    def get_is_subscribed(self, obj):
        if not self.context:
            return 'true'
        user = self.context['request'].user
        if Subscriptions.objects.filter(user=user, follow=obj.id).exists():
            return 'true'
        return 'false'


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.LOGIN_FIELD,
            settings.USER_ID_FIELD,
            "password", 'last_name', 'first_name', 'username'
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'username': {'required': True},
            'email': {'required': True},

        }


class SubscribeRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipes


def get_recipes(obj):
    serializer = SubscribeRecipeSerializer(obj, many=True)
    return serializer.data


class SubscribeSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Subscriptions

    def validate(self, data):
        if data['user'] == data['follow']:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!')
        if Subscriptions.objects.filter(user=data['user'], follow=data['follow']).exists():
            raise serializers.ValidationError('Вы уже подписаны на этого парня!')
        return data

    def to_representation(self, instance):
        follow = CustomUserSerializer(instance.follow).data
        recipes = get_recipes(Recipes.objects.filter(author=instance.follow))
        recipe_count = get_recipes_count(instance.follow)
        result = follow
        result['recipes'] = recipes
        result['recipe_count'] = recipe_count
        return result


def get_recipes_count(obj):
    return len(Recipes.objects.filter(author=obj))


class SubscriptionsSerializer(serializers.ModelSerializer):
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Subscriptions

    def to_representation(self, instance):
        try:
            follow = CustomUserSerializer(instance.follow).data
            recipes_limit = self.context['request'].query_params.get('recipes_limit')
            recipes = get_recipes(Recipes.objects.filter(author=instance.follow)[:int(recipes_limit)])
            recipe_count = get_recipes_count(instance.follow)
            result = follow
            result['recipes'] = recipes
            result['recipe_count'] = recipe_count
            return result
        except:
            follow = CustomUserSerializer(instance.follow).data
            recipes = get_recipes(Recipes.objects.filter(author=instance.follow))
            recipe_count = get_recipes_count(instance.follow)
            result = follow
            result['recipes'] = recipes
            result['recipe_count'] = recipe_count
            return result