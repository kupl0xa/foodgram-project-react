from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter
from recipes.models import Recipe


class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug', lookup_expr='contains'
    )
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.favorite(self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.cart(self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ['tags', 'author']


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'
