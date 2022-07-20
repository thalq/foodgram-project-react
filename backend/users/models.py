from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Length

models.CharField.register_lookup(Length)


class User(AbstractUser):
    """
    Модель пользователя
    """
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        help_text='Обязательное поле.'
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=150, unique=True,
        help_text='Обязательное поле. Имя пользователя должно быть уникальным'
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        help_text='Обязательное поле.'
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        help_text='Обязательное поле.'
    )
    password = models.CharField(
        'Пароль',
        max_length=150,
        help_text='Обязательное поле.'
    )
    subscribing = models.ManyToManyField(
        to='self',
        through='Subscribe',
        symmetrical=False,
        verbose_name='Подписчики',
    )

    class Meta():
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ('username',)
        constraints = (
            models.CheckConstraint(
                check=models.Q(username__length__gte=3),
                name='\nИмя пользователя слишком короткое\n',
            ),
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='\nУникальность пары имя пользователя-адрес email\n',
            ),
        )

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    """
    Модель подписок
    """
    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='subscribers'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='authors'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='\nНельзя подписаться на себя\n',
            ),
        )

    def __str__(self) -> str:
        return f'{self.user} подписан на {self.author}'
