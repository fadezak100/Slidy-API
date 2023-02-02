from rest_framework.test import APITestCase
from .models import User
from knox.models import AuthToken

from django.urls import reverse


class UsersTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='fadezak100',
                                        password='Test123456!!',
                                        email='fadezak100@gmail.com',
                                        first_name='fadi',
                                        last_name='zakout')

        self.token = f'Token {str(AuthToken.objects.create(user=self.user)[1])}'

    def test_get__users(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(reverse('users-list'))
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]['first_name'], 'fadi')

    def test_create_user_with_existed_username(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

        data = {
            "username": "fadezak100",
            "password": "Password123456!!",
            "email": "fadezak100w@gmail.com",
            "first_name": "Micheal",
            "last_name": "Scott"
        }

        response = self.client.post(
            reverse('users-list'), data=data, HTTP_AUTHORIZATION=self.token)
        result = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(result['username'][0], 'This field must be unique.')

    def test_authentication(self):

        self.client.post(reverse('sign-up'), data={
                "username": "ahmedsaleh",
                "password": "Test123456!!",
                "email": "ahmedsaleh@gmail.com",
                "first_name": "Ahmed",
                "last_name": "Saleh"
        })

        credentials = {
            "username": "ahmedsaleh",
            "password": "Test123456!!"
        }

        response = self.client.post(reverse('login'), data=credentials)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result.get('users').get('email'), 'ahmedsaleh@gmail.com')

    def test_logout(self):
        self.client.post(reverse('sign-up'), data={
                "username": "ahmedsaleh",
                "password": "Test123456!!",
                "email": "ahmedsaleh@gmail.com",
                "first_name": "Ahmed",
                "last_name": "Saleh"
        })

        credentials = {
            "username": "ahmedsaleh",
            "password": "Test123456!!"
        }

        response = self.client.post(reverse('login'), data=credentials)
        result = response.json()
        token = result['token']
        token_header = f'Token {token}'

        self.client.credentials(HTTP_AUTHORIZATION=token_header)
        response = self.client.post(reverse('logout')) 
        self.assertEqual(response.status_code, 204)

        # test that the token is invalid
        self.client.credentials(HTTP_AUTHORIZATION=token_header)
        response = self.client.get(reverse('users-list'))
        self.assertEqual(response.status_code, 401)