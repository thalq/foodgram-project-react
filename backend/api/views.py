from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import F, Sum
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserViewSet
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,)

from .filters import RecipeFilter
from .paginators import LimitPageNumberPagination
from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeSerializer, ShortRecipeSerializer,
                          TagSerializer, UserSerializer,
                          UserSubscribeSerializer,)
from recipes.models import Ingredient, IngredientInRecipe, Recipe, Tag

User = get_user_model()


class AddDeleteViewMixin:
    """
    Миксин, позволяющий создавать и удалять подписку/
    рецепт в список покупок/избранный рецепт.
    """
    @action(
        methods=('POST', 'DELETE',),
        detail=True,
    )
    def add_del_obj(self, pk, raw):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=HTTP_401_UNAUTHORIZED)
        raws = {
            'subscribing': user.subscribing,
            'favorites': user.favorites,
            'carts': user.carts,
        }
        raw = raws[raw]
        cur_obj = raw.filter(pk=pk).exists()
        obj = get_object_or_404(self.queryset, pk=pk)
        serializer = self.additional_serializer(
            obj, context={'request': self.request}
        )
        if self.request.method == 'POST' and not cur_obj:
            raw.add(obj)
            return Response(serializer.data, status=HTTP_201_CREATED)
        if self.request.method == 'DELETE' and cur_obj:
            raw.remove(obj)
            return Response(status=HTTP_204_NO_CONTENT)
        return Response(status=HTTP_400_BAD_REQUEST)


class UserViewSet(DjoserViewSet, AddDeleteViewMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitPageNumberPagination
    additional_serializer = UserSubscribeSerializer

    @action(
        methods=('POST', 'DELETE',),
        detail=True,
    )
    def subscribe(self, request, id):
        return self.add_del_obj(id, 'subscribing')

    @action(
        methods=('GET',),
        detail=False,
    )
    def subscriptions(self, request):
        user = request.user
        if user.is_anonymous:
            return Response(status=HTTP_401_UNAUTHORIZED)
        authors = user.subscribing.all()
        pages = self.paginate_queryset(authors)
        serializer = UserSubscribeSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'name'
    search_fields = ('name', )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet, AddDeleteViewMixin):
    queryset = Recipe.objects.select_related('author')
    serializer_class = RecipeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = LimitPageNumberPagination
    additional_serializer = ShortRecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH', 'PUT']:
            return RecipeCreateSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response(
                {"errors": "Такой рецепт существует! Измените название"},
                HTTP_400_BAD_REQUEST
            )

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except IntegrityError:
            return Response(
                {"errors": "Такой рецепт существует! Измените название"},
                HTTP_400_BAD_REQUEST
            )

    @action(
        methods=('POST', 'DELETE',),
        detail=True,
    )
    def shopping_cart(self, request, pk):
        return self.add_del_obj(pk, 'carts')

    @action(methods=('GET',), detail=False)
    def download_shopping_cart(self, request):
        user = self.request.user
        if not user.carts.exists():
            return Response(status=HTTP_400_BAD_REQUEST)
        ingredients = IngredientInRecipe.objects.filter(
            recipe__in=(user.carts.values('id'))
        ).values(
            ingredient_name=F('ingredient__name'),
            measure_unit=F('ingredient__measurement_unit')
        ).annotate(amount_cart=Sum('amount'))
        filename = f'{user.username}_shopping_list.txt'
        shopping_list = ("Список покупок:\n")

        for ing in ingredients:
            shopping_list += (
                f'{ing["ingredient_name"]}: '
                f'{ing["amount_cart"]} '
                f'{ing["measure_unit"]}\n'
            )
        response = HttpResponse(
            shopping_list, content_type='text.txt; charset=utf-8'
        )
        response['Content-Disposition'] = (
            f'attachment; filename={filename}.txt'
        )
        return response

    @action(
        methods=('POST', 'DELETE',),
        detail=True,
    )
    def favorite(self, request, pk):
        return self.add_del_obj(pk, 'favorites')

    @action(
        methods=('GET',),
        detail=False,
    )
    def favorites(self, request):
        user = request.user
        authors = user.favorites.all()
        serializer = RecipeSerializer(
            authors, many=True, context={'request': request}
        )
        return Response(serializer.data)
