# from django.shortcuts import get_object_or_404
# from rest_framework import status
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
# from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class CreateDeleteMixin(CreateModelMixin, DestroyModelMixin,
                        GenericViewSet):
    pass