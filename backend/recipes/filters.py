import django_filters

from recipes.models import Recipe


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.CharFilter(lookup_expr='slug')
    is_favorited = django_filters.filters.BooleanFilter(
        method='get_favorite',
    )
    is_in_shopping_cart = django_filters.filters.BooleanFilter(
        method='get_shop_cart',
    )

    def get_favorite(self, queryset, name, value):
        if self.request.query_params.get('is_favorited'):
            return Recipe.objects.filter(
                favorite_recipe__user=self.request.user)
        return Recipe.objects.all()

    def get_shop_cart(self, queryset, name, value):
        if self.request.query_params.get('is_in_shopping_cart'):
            return Recipe.objects.filter(
                shop_recipe__user=self.request.user)
        return Recipe.objects.all()

    class Meta:
        model = Recipe
        fields = ['author', 'tags']
