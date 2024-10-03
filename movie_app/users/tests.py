from django.test import TestCase
from django.urls import reverse
from .models import CustomUser

class CustomUserTestCase(TestCase):
    def setUp(self):
        # Set up any initial data you need
        CustomUser.objects.create(username="testuser", email="test@example.com", birth_date="1990-01-01", favorite_movie="The Matrix")

    def test_user_creation(self):
        user = CustomUser.objects.get(username="testuser")
        self.assertEqual(user.email, "test@example.com")


    def test_signup_post(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'birth_date': '1995-01-01',
            'favorite_movie': 'Inception',
            'password1': 'compleX1@password',
            'password2': 'compleX1@password'
        }
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, 201) 
        self.assertTrue(CustomUser.objects.filter(username='newuser').exists())
