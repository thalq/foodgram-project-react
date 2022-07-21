from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import get_object_or_404
from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserViewSet
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED)

from api.serializers import (IngredientSerializer, RecipeSerializer,
                             ShortRecipeSerializer, TagSerializer,
                             UserSerializer, UserSubscribeSerializer)

from .mixins import CreateDeleteMixin
from .paginators import LimitPageNumberPagination

User = get_user_model()


class UserViewSet(DjoserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitPageNumberPagination
    additional_serializer = UserSubscribeSerializer

    @action(
        methods=('POST', 'DELETE',),
        detail=True,
    )
    def subscribe(self, request, id):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=HTTP_401_UNAUTHORIZED)
        obj = get_object_or_404(self.queryset, id=id)
        serializer = self.additional_serializer(
            obj, context={'request': self.request}
        )
        if self.request.method == 'POST':
            user.subscribing.add(obj)
            return Response(serializer.data, status=HTTP_201_CREATED)
        if self.request.method == 'DELETE':
            user.subscribing.remove(obj)
            return Response(status=HTTP_204_NO_CONTENT)
        return Response(status=HTTP_400_BAD_REQUEST)
            
    @action(
        methods=('GET',),
        detail=False,
    )
    def subscriptions(self, request):
        user = request.user
        authors = user.subscribing.all()
        pages = self.paginate_queryset(authors)
        if pages:
            serializer = UserSubscribeSerializer(
                pages, many=True, context={'request': request}
            )
            return self.get_paginated_response(serializer.data)
        serializer = UserSubscribeSerializer(
                authors, many=True, context={'request': request}
            )
        return Response(serializer.data)


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


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.select_related('author')
    serializer_class = RecipeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = LimitPageNumberPagination
    additional_serializer = ShortRecipeSerializer
    # filter_backends = (DjangoFilterBackend,)

    @action(
        methods=('POST', 'DELETE',),
        detail=True,
    )
    def favorite(self, request, **kwargs):
        user = self.request.user
        pk = kwargs.get('pk')
        if user.is_anonymous:
            return Response(status=HTTP_401_UNAUTHORIZED)
        obj = get_object_or_404(self.queryset, id=pk)
        serializer = self.additional_serializer(
            obj, context={'request': self.request}
        )
        if self.request.method == 'POST':
            user.favorites.add(obj)
            return Response(serializer.data, status=HTTP_201_CREATED)
        if self.request.method == 'DELETE':
            user.favorites.remove(obj)
            return Response(status=HTTP_204_NO_CONTENT)
        return Response(status=HTTP_400_BAD_REQUEST)

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
