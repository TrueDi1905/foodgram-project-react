from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from .serializers import CustomUserSerializer, UserSubscriptionsSerializer
from .models import UserSubscriptions
User = get_user_model()


class UserPaginator(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    pagination_class = UserPaginator


class UserSubscriptionsView(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = UserSubscriptions.objects.all()
    serializer_class = UserSubscriptionsSerializer()