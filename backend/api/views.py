from django.contrib.auth import get_user_model

from djoser.views import UserViewSet as DjoserViewSet
from rest_framework import viewsets, permissions, filters
from django_filters import rest_framework
from rest_framework.decorators import action

from .serializers import TagSerializer, UserSerializer, IngredientSerializer, SubscribeSerializer
from recipes.models import Tag, Ingredient
from users.models import Subscribe
from .mixins import CreateDeleteMixin

User = get_user_model()


class UserViewSet(DjoserViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    @action(detail=True, methods=['get', 'delete'],
            serializer_class=SubscribeSerializer,
            permission_classes=[permissions.IsAuthenticated]
            )
    def subscribe(self, request, id=None):
        user = self.request.user
        author = self.get_object()


class SubscribeViewSet(CreateDeleteMixin):
    serializer_class = SubscribeSerializer
    filter_backends = (rest_framework.DjangoFilterBackend,)
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Subscribe.objects.filter(
            subscriber=user).select_related('subscriber')


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
