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
