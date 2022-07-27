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
        max_length=150,
        unique=True,
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
        symmetrical=False,
        verbose_name='Подписчики',
    )

    class Meta():
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)
        constraints = (
            models.CheckConstraint(
                check=models.Q(username__length__gte=3),
                name='\nИмя пользователя слишком короткое\n',
            ),
            models.UniqueConstraint(
                fields=('username', 'email',),
                name='\nУникальность пары имя пользователя-адрес email\n',
            ),
        )

    def __str__(self):
        return self.username
