from django.contrib import admin
from .models import NutritionCategory, MealRecipe

class MealRecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'category', 'created_at', 'image')
    list_filter = ('category', 'user')
    search_fields = ('name', 'user__username', 'ingredients', 'description')
    # readonly_fields = ('created_at', 'updated_at') # If status field was present and handled by workflow

admin.site.register(NutritionCategory)
admin.site.register(MealRecipe, MealRecipeAdmin)
