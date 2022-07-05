from django.contrib import admin, auth

from .models import User


@admin.register(User)
class UserAdmin(auth.admin.UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    fields = (('first_name', 'last_name'), ('username', 'email'))
    fieldsets = []
    search_fields = ('username', 'email')
    list_filter = ('first_name', 'email')
    save_on_top = True
