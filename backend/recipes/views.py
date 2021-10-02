import django_filters
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework import filters
from django_filters import rest_framework as filter
from users.views import UserPagination
from .serializers import TagSerializer, IngredientsSerializer, RecipeSerializer, FavoriteRecipesSerializer, \
    ShoppingSerializers, CreateRecipeSerializer
from .models import Tags, Ingredients, Recipes, FavoriteRecipes, ShoppingCart
from rest_framework.decorators import action
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas


class TagList(viewsets.ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagSerializer


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.CharFilter(lookup_expr='slug')

    class Meta:
        model = Recipes
        fields = ['author', 'tags',]


class IngredientsList(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = UserPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (filter.DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action == 'favorite':
            return FavoriteRecipesSerializer
        if self.action == 'shopping_cart':
            return ShoppingSerializers
        return RecipeSerializer

    def get_queryset(self):
        if self.request.query_params.get('is_favorited') == '1':
            self.queryset = Recipes.objects.filter(favorite_recipe__user=self.request.user)
        if self.request.query_params.get('is_in_shopping_cart') == '1':
            self.queryset = Recipes.objects.filter(shop_recipe__user=self.request.user)
        return self.queryset

    def create(self, request, *args, **kwargs):
        serializer = CreateRecipeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['GET', 'DELETE'], permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        user = request.user.id
        recipe = get_object_or_404(Recipes, id=pk)
        if request.method == 'GET':
            data = {'user': user, 'recipe': pk}
            serializer = self.get_serializer(data=data, context={'request': request, 'recipe': recipe})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        recipe_follow = FavoriteRecipes.objects.filter(user=user, recipe=recipe)
        if not recipe_follow:
            return Response({
                'errors': 'Вы не добавляли этот рецепт!'
            }, status=status.HTTP_400_BAD_REQUEST)
        recipe_follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['GET', 'DELETE'], permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        user = request.user.id
        recipe = get_object_or_404(Recipes, id=pk)
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
        result = 'Надо доделать'
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 100, result)
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='shopping_cart.pdf')
