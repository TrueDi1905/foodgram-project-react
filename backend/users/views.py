from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from djoser.views import UserViewSet
from .models import Subscriptions
from .serializers import CustomUserSerializer, SubscriptionsSerializer
from .serializers import SubscribeSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    pagination_class = LimitOffsetPagination #также нужно добавить пагинацию по страницам

    def get_serializer_class(self):
        if self.action == 'subscriptions':
            return SubscriptionsSerializer
        if self.action == 'subscribe':
            return SubscribeSerializer
        return CustomUserSerializer

    @action(detail=False)
    def subscriptions(self, request):
        follow = Subscriptions.objects.filter(user=request.user)
        serializer = self.get_serializer(follow, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET', 'DELETE'])
    def subscribe(self, request, id):
        user = request.user.id
        follow = get_object_or_404(User, id=id)
        if request.method == 'GET':
            data = {'user': user, 'follow': id}
            serializer = self.get_serializer(data=data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        follow = Subscriptions.objects.filter(user=user, follow=follow)
        if not follow:
            return Response({
                'errors': 'Вы не подписаны на этого парня!'
            }, status=status.HTTP_400_BAD_REQUEST)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
