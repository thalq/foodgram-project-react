from django.contrib import admin

from .models import Ingredient, IngredientInRecipe, Recipe, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')
    fields = ('name', 'slug', 'color')
    search_fields = ('name', 'slug')
    list_filter = ('name', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    fields = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)


class IngredientInRecipeInline(admin.TabularInline):
    model = IngredientInRecipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name', 'tags', 'image', 'text', 'cooking_time', 'author')
    search_fields = ('name', 'tags')
    list_filter = ('name', 'tags')
    inlines = [IngredientInRecipeInline]
    