from django.contrib.admin import register
from django.contrib.auth import admin

from .models import User


@register(User)
class UserAdmin(admin.UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    fields = (('first_name', 'last_name'), ('username', 'email'))
    fieldsets: list = []
    search_fields = ('username', 'email')
    list_filter = ('first_name', 'email')
    save_on_top = True
