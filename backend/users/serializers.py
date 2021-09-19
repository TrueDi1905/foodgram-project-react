from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
User = get_user_model()
from djoser.conf import settings
from .models import UserSubscriptions


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


class UserSubscriptionsSerializer(serializers.ModelSerializer):
     class Meta:
         model = UserSubscriptions
         fields = '__all__'
         depth = 1