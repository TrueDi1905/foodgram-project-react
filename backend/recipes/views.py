from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .serializers import TagSerializer, IngredientsSerializer, RecipeSerializer, FavoriteRecipesSerializer
from .models import Tags, Ingredients, Recipes, FavoriteRecipes


class RecipePaginator(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class TagList(viewsets.ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagSerializer


class IngredientsList(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = RecipePaginator


class FavoriteRecipesView(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = FavoriteRecipes.objects.all()
    serializer_class = FavoriteRecipesSerializer

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipes, pk=self.kwargs.get('pk'))
        serializer.save(user=self.request.user, recipe=recipe)

    def destroy(self, request, *args, **kwargs):
        instance = FavoriteRecipes.objects.filter(user=self.request.user, recipe=self.kwargs.get('pk'))
        if len(instance) == 0:
            raise ValidationError('Рецепта не был добавлен')
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
