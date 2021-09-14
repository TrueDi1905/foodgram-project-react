from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from .models import Tags, Ingredients, Recipes
from .serializers import TagSerializer, IngredientsSerializer, RecipeSerializer


class TagList(viewsets.ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagSerializer


class IngredientsList(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipeSerializer
