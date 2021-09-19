from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('tags', views.TagList, basename='tags')
router.register('ingredients', views.IngredientsList, basename='ingredients')
router.register('recipes', views.RecipesViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path('recipes/<int:pk>/favorite/', views.FavoriteRecipesView.as_view({'get': 'create', 'delete': 'destroy'}))
]
