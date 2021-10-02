from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('tags', views.TagList, basename='tags')
router.register('ingredients', views.IngredientsList, basename='ingredients')
router.register(r'recipes', views.RecipesViewSet, basename='recipes')

urlpatterns = router.urls
