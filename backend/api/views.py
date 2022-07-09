from django.contrib.auth import get_user_model

from djoser.views import UserViewSet as DjoserViewSet

from .serializers import UserSerializer 

User = get_user_model()


class UserViewSet(DjoserViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

