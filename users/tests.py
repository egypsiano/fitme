from django.test import TestCase
from .calculators import (
    calculate_bmi,
    calculate_bmr_mifflin_st_jeor,
    calculate_daily_calorie_needs,
    ACTIVITY_LEVELS
)
from django.urls import reverse
from .models import User # Required for UserViewTests

class CalculatorTests(TestCase):
    def test_calculate_bmi(self):
        self.assertAlmostEqual(calculate_bmi(weight_kg=70, height_cm=175), 22.86)
        self.assertAlmostEqual(calculate_bmi(weight_kg=60, height_cm=160), 23.44)
        self.assertIsNone(calculate_bmi(weight_kg=0, height_cm=175))
        self.assertIsNone(calculate_bmi(weight_kg=70, height_cm=0))
        self.assertIsNone(calculate_bmi(weight_kg=None, height_cm=175))
        self.assertIsNone(calculate_bmi(weight_kg=70, height_cm=None))

    def test_calculate_bmr_mifflin_st_jeor(self):
        # Men: (10 * weight) + (6.25 * height) - (5 * age) + 5
        # Women: (10 * weight) + (6.25 * height) - (5 * age) - 161
        self.assertAlmostEqual(calculate_bmr_mifflin_st_jeor(70, 175, 30, 'M'), 1648.75) # Corrected: (10*70) + (6.25*175) - (5*30) + 5 = 700 + 1093.75 - 150 + 5 = 1648.75
        self.assertAlmostEqual(calculate_bmr_mifflin_st_jeor(60, 165, 25, 'F'), 1345.25) # Corrected: (10*60) + (6.25*165) - (5*25) - 161 = 600 + 1031.25 - 125 - 161 = 1345.25
        self.assertIsNone(calculate_bmr_mifflin_st_jeor(70, 175, 30, 'O')) # Other sex
        self.assertIsNone(calculate_bmr_mifflin_st_jeor(None, 175, 30, 'M'))

    def test_calculate_daily_calorie_needs(self):
        bmr = 1600
        self.assertAlmostEqual(calculate_daily_calorie_needs(bmr, 'SEDENTARY'), 1920) # 1600 * 1.2
        self.assertAlmostEqual(calculate_daily_calorie_needs(bmr, 'LIGHT'), 2200)     # 1600 * 1.375
        self.assertAlmostEqual(calculate_daily_calorie_needs(bmr, 'MODERATE'), 2480)  # 1600 * 1.55
        self.assertAlmostEqual(calculate_daily_calorie_needs(bmr, 'ACTIVE'), 2760)    # 1600 * 1.725
        self.assertAlmostEqual(calculate_daily_calorie_needs(bmr, 'VERY_ACTIVE'), 3040) # 1600 * 1.9
        self.assertIsNone(calculate_daily_calorie_needs(bmr, 'INVALID_KEY'))
        self.assertIsNone(calculate_daily_calorie_needs(None, 'SEDENTARY'))

class UserViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='viewuser', password='password123', email='view@test.com')

    def test_login_page_loads(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_register_page_loads(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_profile_view_authenticated(self):
        self.client.login(username='viewuser', password='password123')
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_profile_view_redirects_if_not_authenticated(self):
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 302) # Redirects to login
        # Corrected redirect assertion to use the actual login URL from settings or default
        # Assuming default login URL name is 'login' from django.contrib.auth.urls
        # If using a custom login URL name within an app namespace, adjust accordingly.
        # The prompt setup uses 'users:login' for app-specific login, but global 'login' for redirects.
        # Django's @login_required redirects to settings.LOGIN_URL which defaults to '/accounts/login/'
        # This URL is typically named 'login'.
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('users:profile'))
