from django.contrib.auth import get_user_model

from djoser.views import UserViewSet as DjoserViewSet
from rest_framework import viewsets, permissions

from .serializers import TagSerializer, UserSerializer, IngredientSerializer
from recipes.models import Tag, Ingredient

User = get_user_model()


class UserViewSet(DjoserViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer