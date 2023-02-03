from django.contrib import admin
from .models import Cart, Favorite, Ingredient, IngredientRecipe, Recipe, Tag


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through


class RecipeModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'get_favorite_count']
    list_filter = ['name', 'author', 'tags']
    inlines = (IngredientInline,)

    @staticmethod
    def get_favorite_count(obj):
        return obj.favorites.count()


class IngredientModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'measurement_unit']
    list_filter = ['name']


admin.site.register(Cart)
admin.site.register(Favorite)
admin.site.register(Ingredient, IngredientModelAdmin)
admin.site.register(IngredientRecipe)
admin.site.register(Recipe, RecipeModelAdmin)
admin.site.register(Tag)
