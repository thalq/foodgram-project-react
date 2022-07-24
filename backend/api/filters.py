from django_filters.rest_framework import ChoiceFilter, FilterSet, filters
from recipes.models import Ingredient, Recipe

RECIPE_CHOICES = (
    (0, 'False'),
    (1, 'True'),
)

class RecipeFilter(FilterSet):
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug',
    )
    author = filters.AllValuesFilter(
        field_name='author__username',
    )
    is_in_shopping_cart = ChoiceFilter(
        choices=RECIPE_CHOICES,
        method='get_is_in'
    )
    is_favorited = filters.ChoiceFilter(
        choices=RECIPE_CHOICES,
        method='get_is_in'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def get_is_in(self, queryset, name, value):
        """
        Фильтрация рецептов по избранному и списку покупок.
        """
        user = self.request.user
        if value == '1':
            if name == 'is_favorited':
                queryset = queryset.filter(favorite=user)
            if name == 'is_in_shopping_cart':
                queryset = queryset.filter(cart=user)
        return queryset
