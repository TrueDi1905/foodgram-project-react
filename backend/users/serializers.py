from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.validators import UniqueTogetherValidator
from .models import Subscriptions
User = get_user_model()
from djoser.conf import settings

class CustomUserSerializer(UserSerializer):

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD, 'last_name', 'first_name', 'email', 'username')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
        }


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


class SubscribeSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()

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

    def get_recipes(self, obj):
        recipe = obj.follow.recipes
        return recipe


class SubscriptionsSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        models = Subscriptions
