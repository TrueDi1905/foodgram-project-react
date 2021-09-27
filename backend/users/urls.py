from django.contrib.auth import get_user_model
from django.urls import path, include

from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', views.CustomUserViewSet)

User = get_user_model()

urlpatterns = router.urls
