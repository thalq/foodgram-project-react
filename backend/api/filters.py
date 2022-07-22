from django_filters import rest_framework as filters
from recipes.models import Recipe, Tag


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class RecipeFilter(filters.FilterSet):
    """
    Для фильтрации по избранному, автору, списку
    покупок и тегам.
    """
    author = CharFilterInFilter(field_name='author__username', lookup_expr='in')
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = filters.BooleanFilter(
        field_name='favorite'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='cart'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')
