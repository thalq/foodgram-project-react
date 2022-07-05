from rest_framework import viewsets
from users.models import User
from djoser.views import UserViewSet as DjoserViewSet
from .serializers import UserSerializer 

class UserViewSet(DjoserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer  
