from django.db import models
from django.conf import settings # To get AUTH_USER_MODEL

class NutritionCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Nutrition Categories'

class MealRecipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='meal_recipes')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    ingredients = models.TextField(help_text='List each ingredient on a new line.')
    instructions = models.TextField(help_text='Provide step-by-step instructions.')

    prep_time_minutes = models.PositiveIntegerField(null=True, blank=True, help_text='Preparation time in minutes.')
    cook_time_minutes = models.PositiveIntegerField(null=True, blank=True, help_text='Cooking time in minutes.')
    servings = models.PositiveIntegerField(null=True, blank=True, help_text='Number of servings.')

    category = models.ForeignKey(NutritionCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='recipes')
    image = models.ImageField(upload_to='meal_recipe_images/', null=True, blank=True, help_text='Upload an image of the meal.')
    # video_url for cooking instructions could be added later if needed.

    # status = models.CharField(max_length=10, choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved')], default='APPROVED') # If moderation is needed later for user submissions

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Meal Recipes'

# UserMealUpload model is removed for now, users directly create MealRecipe.
# If detailed user uploads with moderation distinct from recipes are needed, it can be re-added.
