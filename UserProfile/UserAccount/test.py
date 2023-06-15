from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import UserModel
from .serializers import ProfileEditSerializer

class UserSignupViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('user-signup')

    def test_user_signup_success(self):
        data = {
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Account created successfully')

    def test_user_signup_invalid_email(self):
        data = {
            'email': 'invalid_email',
            'password': 'testpassword'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Invalid email format')


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('login')

    def test_login_success(self):
        # Create a test user
        user = UserModel.objects.create(email='test@example.com')
        user.set_password('testpassword')
        user.save()

        data = {
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertEqual(response.data['message'], 'Login successfully')

    def test_login_invalid_credentials(self):
        data = {
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Account not found')


class CreateProfileViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('create-profile')

    def test_create_profile_authenticated_user(self):
        # Create a test user
        user = UserModel.objects.create(email='test@example.com')

        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'bio': 'Hello, I am John Doe.',
            'profile_picture': 'http://example.com/profile.jpg'
        }

        # Authenticate the user
        self.client.force_authenticate(user=user)

        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Profile Updated successfully')

    def test_create_profile_unauthenticated_user(self):
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'bio': 'Hello, I am John Doe.',
            'profile_picture': 'http://example.com/profile.jpg'
        }

        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
