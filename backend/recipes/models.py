from django.core.validators import (MaxValueValidator, MinLengthValidator,
                                    MinValueValidator, RegexValidator,
                                    validate_slug,)
from django.db import models

from colorfield.fields import ColorField

from users.models import User


class Tag(models.Model):
    """
    Модель для тегов.
    """
    name = models.CharField(
        'Имя',
        max_length=200,
        unique=True,
        validators=[
            MinLengthValidator(1, 'Введите название тэга'),
        ],

    )
    slug = models.SlugField(
        'Слаг',
        max_length=200,
        unique=True,
        validators=[
            MinLengthValidator(3, 'Должно состоять минимум из 3х символов'),
            validate_slug,
        ]
    )
    color = color = ColorField(default='#FF0000')

    class Meta():
        verbose_name = 'тег'
        verbose_name_plural = 'теги'
        ordering = ('name',)

    def save(self, *args, **kwargs):
        """
        Превод слага в нижний регистр при сохранении
        """
        self.slug = self.slug.lower()
        return super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Модель для ингредиентов.
    """
    name = models.CharField(
        'Название иградиента',
        max_length=200,
        validators=[
            MinLengthValidator(
                3, 'Название ингредиента должно быть более 3х символов'
            )
        ]
    )
    measurement_unit = models.CharField(
        'Ед. измерения',
        max_length=200,
        validators=[
            MinLengthValidator(
                1, 'Введите единицу измерения'
            )
        ]
    )

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
    """
    Модель для рецептов.
    """
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        verbose_name='Ингредиенты',
        related_name='recipes'
    )
    tags = models.ManyToManyField(
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
    name = models.CharField(
        'Название',
        max_length=200,
        validators=(
            MinLengthValidator(
                1, 'Название рецепта слишком короткое'
            ),
            RegexValidator(
                '^[a-zA-Zа-яА-Я ]+$',
                (
                    'Название рецепта содержит недопустимые символы'
                )
            )
        )
    )
    text = models.TextField('Описание рецепта',)
    cooking_time = models.PositiveIntegerField(
        'Время приготовления в минутах',
        validators=(
            MinValueValidator(
                1,
                'Минимальное значение 1 минута'
            ),
            MaxValueValidator(
                300,
                'Максимальное значение 300 минут'
            ),
            RegexValidator(
                '^[0-9]+$',
                (
                    'Время приготовления может быть '
                    'только числом от 1 до 300'
                )
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
    """
    модель для ингредиентов в рецепте.
    """
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='ingredients_amount',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='ingredients_in_recipe',
    )
    amount = models.PositiveIntegerField(
        'Количество',
        default=0,
        validators=(
            MinValueValidator(
                1, 'Минимальное значение 1'
            ),
            MaxValueValidator(
                10000, 'Максимальное значение 10000'
            ),
            RegexValidator(
                '^[0-9]+$',
                (
                    'Количество ингредиента может быть '
                    'только числом от 1 до 10000'
                )
            ),
        ),
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        ordering = ('-pk',)

    def __str__(self):
        return (
            f'{self.ingredient}'
            f'{self.amount} {self.ingredient.measurement_unit}'
        )
