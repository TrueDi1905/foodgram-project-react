from django_filters import rest_framework as filters

from recipes.models import Recipe


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class RecipeFilter(filters.FilterSet):
    tags = CharFilterInFilter(
        field_name='tags__slug', lookup_expr='in')
    author = filters.NumberFilter(lookup_expr='id')
    is_favorited = filters.filters.BooleanFilter(
        method='get_favorite',
    )
    is_in_shopping_cart = filters.filters.BooleanFilter(
        method='get_shop_cart',
    )

    def get_favorite(self, queryset, name, value):
        if self.request.query_params.get('is_favorited'):
            return queryset.filter(
                favorite_recipe__user=self.request.user
            )
        return queryset

    def get_shop_cart(self, queryset, name, value):
        if self.request.query_params.get('is_in_shopping_cart'):
            return queryset.filter(
                shop_recipe__user=self.request.user
            )
        return queryset

    class Meta:
        model = Recipe
        fields = ['author', 'tags']
