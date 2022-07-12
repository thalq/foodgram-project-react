from unicodedata import name
from django.db import models


class Tag(models.Model):
    name = models.CharField('Имя', max_length=200, unique = True)
    slug = models.SlugField('Слаг', max_length=200, unique = True)
    color = models.CharField('Цвет', max_length=6, null = True, blank=True)

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
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'
        ordering = ('name',)
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='\nТакой ингредиент уже есть\n'
            ),
        )

    def __str__(self):
        return self.name