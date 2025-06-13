from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import NutritionCategory, MealRecipe

User = get_user_model()

class NutritionViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='nutritionuser', password='password123')
        self.category = NutritionCategory.objects.create(name='Healthy Snacks')
        self.recipe = MealRecipe.objects.create(user=self.user, name='Fruit Salad', ingredients='Apple, Banana', instructions='Mix them.')

    def test_recipe_list_view(self):
        response = self.client.get(reverse('nutrition:recipe_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nutrition/recipe_list.html')

    def test_recipe_detail_view(self):
        response = self.client.get(reverse('nutrition:recipe_detail', args=[self.recipe.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nutrition/recipe_detail.html')

    def test_add_recipe_view_redirects_if_not_authenticated(self):
        response = self.client.get(reverse('nutrition:add_recipe'))
        self.assertEqual(response.status_code, 302)
