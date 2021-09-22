from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet

from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response

from .serializers import CustomUserSerializer
from .models import Subscriptions
from .serializers import SubscribeSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    pagination_class = LimitOffsetPagination #также нужно добавить пагинацию по страницам

    @action(
        ["post"], detail=False, url_path="reset_{}_confirm".format(User.USERNAME_FIELD)
    )
    def reset_username_confirm(self, request, *args, **kwargs):
        raise ValidationError({'error': 'Недоступно'})

    @action(["post"], detail=False, url_path="reset_{}".format(User.USERNAME_FIELD))
    def reset_username(self, request, *args, **kwargs):
        raise ValidationError({'error': 'Недоступно'})

    @action(["post"], detail=False, url_path="set_{}".format(User.USERNAME_FIELD))
    def set_username(self, request, *args, **kwargs):
        raise ValidationError({'error': 'Недоступно'})

    @action(["post"], detail=False)
    def reset_password_confirm(self, request, *args, **kwargs):
        raise ValidationError({'error': 'Недоступно'})

    @action(["post"], detail=False)
    def reset_password(self, request, *args, **kwargs):
        raise ValidationError({'error': 'Недоступно'})

    @action(["post"], detail=False)
    def resend_activation(self, request, *args, **kwargs):
        raise ValidationError({'error': 'Недоступно'})

    @action(["post"], detail=False)
    def activation(self, request, *args, **kwargs):
        raise ValidationError({'error': 'Недоступно'})


class SubscribeView(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Subscriptions.objects.all()
    serializer_class = SubscribeSerializer

    def create(self, request, *args, **kwargs):
        if len(User.objects.filter(id=self.kwargs.get('id'))) == 0:
            Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        follow = get_object_or_404(User, id=self.kwargs.get('id'))
        serializer.save(user=self.request.user, follow=follow)

    def destroy(self, request, *args, **kwargs):
        if len(User.objects.filter(id=self.kwargs.get('id'))) == 0:
            Response(status=status.HTTP_404_NOT_FOUND)
        follow = get_object_or_404(User, id=self.kwargs.get('id'))
        instance = Subscriptions.objects.filter(user=self.request.user, follow=follow)
        if len(instance) == 0:
            raise ValidationError('нет такого парня')
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionsView(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Subscriptions.objects.all()
    serializer_class = SubscribeSerializer
