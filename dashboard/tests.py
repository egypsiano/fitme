from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class DashboardViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='dashuser', password='password123')

    def test_dashboard_view_authenticated(self):
        self.client.login(username='dashuser', password='password123')
        response = self.client.get(reverse('dashboard:user_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/dashboard.html')

    def test_dashboard_view_redirects_if_not_authenticated(self):
        response = self.client.get(reverse('dashboard:user_dashboard'))
        self.assertEqual(response.status_code, 302)
