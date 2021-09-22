from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer

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
    user = serializers.StringRelatedField()
    follow = serializers.StringRelatedField()

    class Meta:
        fields = '__all__'
        model = Subscriptions

    def validate(self, attrs):
        user = User.objects.get(id=self.context['request'].user.id)
        follow = User.objects.get(
            id=self.context['view'].kwargs.get('id')
        )
        if Subscriptions.objects.filter(user=user, follow=follow).exists():
            raise serializers.ValidationError("Вы уже подписаны на этого парня!")
        if user == follow:
            raise serializers.ValidationError("На себя нельзя подписаться!")
        else:
            return attrs
