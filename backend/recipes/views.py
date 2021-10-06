import io
import django_filters
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework import filters
from django_filters import rest_framework as filter
from users.views import UserPagination
from .filters import RecipeFilter
from .serializers import TagSerializer, IngredientSerializer, RecipeSerializer, FavoriteRecipeSerializer, \
    ShoppingSerializers
from .models import Tag, Ingredient, Recipe, FavoriteRecipe, ShoppingCart
from rest_framework.decorators import action
from django.http import FileResponse, HttpResponse
from reportlab.pdfgen import canvas


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
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (filter.DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action == 'favorite':
            return FavoriteRecipeSerializer
        if self.action == 'shopping_cart':
            return ShoppingSerializers
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['GET', 'DELETE'], permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        user = request.user.id
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'GET':
            data = {'user': user, 'recipe': pk}
            serializer = self.get_serializer(data=data, context={'request': request, 'recipe': recipe})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        recipe_follow = FavoriteRecipe.objects.filter(user=user, recipe=recipe)
        if not recipe_follow:
            return Response({
                'errors': 'Вы не добавляли этот рецепт!'
            }, status=status.HTTP_400_BAD_REQUEST)
        recipe_follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['GET', 'DELETE'], permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        user = request.user.id
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'GET':
            data = {'user': user, 'recipes_shop': pk}
            serializer = self.get_serializer(data=data, context={'request': request, 'recipes_shop': recipe})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        recipe_follow = ShoppingCart.objects.filter(user=user, recipes_shop=recipe)
        if not recipe_follow:
            return Response({
                'errors': 'Вы не добавляли этот рецепт в список покупок!'
            }, status=status.HTTP_400_BAD_REQUEST)
        recipe_follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False)
    def download_shopping_cart(self, request):
        recipe = get_object_or_404(ShoppingCart, user=request.user)
        result = []
        result += str(recipe.recipes_shop.name)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
        p = canvas.Canvas(response)
        p.drawString(100, 100, result)
        p.showPage()
        p.save()
        return response
