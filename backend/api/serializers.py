from string import hexdigits

from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Ingredient, IngredientInRecipe, Recipe, Tag
from rest_framework import serializers
from rest_framework.serializers import ValidationError

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'password'
        )
        extra_kwargs = {'password': {'write_only':True}}
        read_only_fields = ('is_subscribed', )
    
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.subscribing.filter(id=obj.id).exists()


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = 'id', 'name', 'image', 'cooking_time', 
        read_only_fields = '__all__',


class UserSubscribeSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
        read_only_fields = '__all__',

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        query_params = self.context.get('request').query_params
        recipes_limit = query_params.get('recipes_limit', False)
        if recipes_limit:
            recipes_limit = int(recipes_limit)
            recipes = Recipe.objects.filter(author=obj)[:recipes_limit]
        else:
            recipes = Recipe.objects.filter(author=obj)
        serializer = ShortRecipeSerializer(recipes, many=True)
        return serializer.data

    def validate_subscription(self, value):
        request = self.context['request']
        if not request.user == value:
            return value
        raise serializers.ValidationError(
            'Вы не можете подписаться на себя'
        )


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

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientsInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        source='ingredient.id'
    )
    name = serializers.CharField(
        source='ingredient.name'
    )
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )
    amount = serializers.IntegerField(source='amount')

    class Meta:
        model = IngredientInRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )
        read_only_fields = ("name", "measurement_unit")


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientSerializer(read_only=True, many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    # image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        read_only_fields = (
            'is_favorite',
            'is_shopping_cart',
        )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorites.filter(id=obj.id).exists()

    # def create(self, validated_data):

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            IngredientInRecipe.objects.get_or_create(
                recipe=recipe,
                ingredients=ingredient['ingredient'],
                amount=ingredient['amount']
            )

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.carts.filter(id=obj.id).exists()

            
