from string import hexdigits

from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from recipes.models import Tag

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only':True}}
    
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug', 'color')
        read_only_fields = ('id', 'name', 'slug', 'color')

    def validate_color(self, color):
        color = str(color).strip('#')
        if len(color) not in (3,6):
            raise ValidationError(
                f'Длина должна быть 3 или 6 символов, а не {len(color)}'
            )
        if not set(color).issubset(hexdigits):
            raise ValidationError(
                'Строка содержит недопустимый символ'
            )