from django.core.validators import MinValueValidator
from django.db import models
from foodgram.constants import MIN_COOKING_TIME
from users.models import User


class Tag(models.Model):
    name = models.CharField('Имя', max_length=200, unique = True)
    slug = models.SlugField('Слаг', max_length=200, unique = True)
    color = models.CharField('Цвет', max_length=7, null = True, blank=True)

    class Meta():
        verbose_name = 'тег'
        verbose_name_plural = 'теги'
        ordering = ('name',)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField('Название иградиента', max_length=200)
    measurement_unit = models.CharField('Ед. измерения', max_length=200)

    class Meta():
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='\nТакой ингредиент уже есть\n'
            ),
        )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        verbose_name='Ингредиенты',
        related_name='recipes'
    )
    tags  = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги',
    )
    author = models.ForeignKey(
        verbose_name='Автор рецепта',
        related_name='recipes',
        to=User,
        on_delete=models.CASCADE,
    )
    favorite = models.ManyToManyField(
        verbose_name='Избранные рецепты',
        related_name='favorites',
        to=User,
    )
    cart = models.ManyToManyField(
        verbose_name='Список покупок',
        related_name='carts',
        to=User,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    image = models.ImageField('Изображение', upload_to='images/')
    name = models.CharField('Название', max_length=200)
    text = models.TextField('Описание рецепта',)
    cooking_time = models.PositiveIntegerField(
        'Время приготовления в минутах',
        validators=(
            MinValueValidator(
                MIN_COOKING_TIME,
                'Время приготовления не может быть менее одной минуты.'
            ),
        ),
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pk',)
    
    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='ingredients_in_recipe',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='ingredients_in_recipe',
    )
    amount = models.PositiveIntegerField(
        'Количество',
        default=0
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        ordering = ('-pk',)
        
    
    def __str__(self):
        return (
            f'{self.ingredient.name}'
            f'{self.amount} {self.ingredient.measurement_unit}'
        )


