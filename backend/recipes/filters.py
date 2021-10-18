import django_filters


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.CharFilter(name='tags', lookup_expr='slug')
    author = django_filters.NumberFilter(lookup_expr='id')
    is_favorited = django_filters.filters.BooleanFilter(
        method='get_favorite',
    )
    is_in_shopping_cart = django_filters.filters.BooleanFilter(
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
