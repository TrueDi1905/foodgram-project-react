from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filter
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from users.views import UserPagination
from .filters import RecipeFilter
from .models import (FavoriteRecipe, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)
from .permissions import IsAuthorOrAdmin
from .serializers import (FavoriteRecipeSerializer, IngredientSerializer,
                          RecipeSerializer, ShoppingSerializers, TagSerializer,
                          RecipeGetSerializer)


class TagList(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientList(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = UserPagination
    permission_classes = [IsAuthorOrAdmin]
    filter_backends = (filter.DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action == 'favorite':
            return FavoriteRecipeSerializer
        if self.action == 'shopping_cart':
            return ShoppingSerializers
        if self.request.method == 'GET':
            return RecipeGetSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['GET', 'DELETE'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        user = request.user.id
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'GET':
            data = {'user': user, 'recipe': pk}
            serializer = self.get_serializer(
                data=data, context={'request': request, 'recipe': recipe})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        recipe_follow = FavoriteRecipe.objects.filter(
            user=user,
            recipe=recipe)
        if not recipe_follow:
            return Response({
                'errors': 'Вы не добавляли этот рецепт!'
            }, status=status.HTTP_400_BAD_REQUEST)
        recipe_follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['GET', 'DELETE'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        user = request.user.id
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'GET':
            data = {'user': user, 'recipes_shop': pk}
            serializer = self.get_serializer(
                data=data,
                context={'request': request, 'recipes_shop': recipe})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        recipe_follow = ShoppingCart.objects.filter(
            user=user, recipes_shop=recipe)
        if not recipe_follow:
            return Response({
                'errors': 'Вы не добавляли этот рецепт в список покупок.'
            }, status=status.HTTP_400_BAD_REQUEST)
        recipe_follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False)
    def download_shopping_cart(self, request):
        shop_list = IngredientAmount.objects.filter(
            recipes__shop_recipe__user=request.user).values(
            'ingredients__name',
            'ingredients__measurement_unit'
        ).annotate(amount=Sum('amount'))
        result_sale = ''
        for ingredient in shop_list:
            result_sale += (
                f'{ingredient["ingredients__name"]} - '
                f'{str(ingredient["amount"])} - '
                f'{ingredient["ingredients__measurement_unit"]}. ')
        download = 'sales_list.txt'
        response = HttpResponse(
            result_sale, content_type="text/plain,charset=utf8")
        response['Content-Disposition'] = (
            'attachment; filename={0}'.format(download)
        )
        return response
