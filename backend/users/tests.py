from rest_framework.test import APITestCase

from .models import User
from knox.models import AuthToken

from django.urls import reverse


class UsersTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='fadezak100',
            password='Test123456!!',
            email='fadezak100@gmail.com',
            first_name='fadi',
            last_name='zakout'
        )

        self.token = f'Token {str(AuthToken.objects.create(user=self.user)[1])}'

    def test_get_users_without_slides(self):
        response = self.client.get(reverse('users-list'))
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]['first_name'], 'fadi')

    def test_get_users_with_slides(self):
        response = self.client.get(reverse('users-list') + '?slides=true')
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]['first_name'], 'fadi')
        self.assertIn('slides_data', result[0])
        self.assertIsInstance(result[0]['slides_data'], list)

    def test_create_user_with_existed_username_throws_exception(self):
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

    def test_authentication_flow(self):
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
        self.assertEqual(result.get('users').get(
            'email'), 'ahmedsaleh@gmail.com')

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

        self.client.credentials(HTTP_AUTHORIZATION=token_header)
        response = self.client.get(reverse('users-list'))
        self.assertEqual(response.status_code, 401)

    def test_login_with_slides(self):
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
        response = self.client.post(
            reverse('login') + '?slides=true', data=credentials)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('slides_data', result['users'])
        self.assertIsInstance(result['users']['slides_data'], list)

    def test_login_without_slides(self):
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
        self.assertNotIn('slides_data', result['users'])

    def test_update_own_avatar(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

        data = {
            "avatar": "https://pbs.twimg.com/profile_banners/1236621082213462016/1674966722/1500x500"
        }

        response = self.client.put(
            reverse('users-detail', kwargs={'pk': self.user.id}), data=data)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['data']['avatar'], data['avatar'])


    def test_update_other_avatar_throws_exception(self):
        new_user_response = self.client.post(reverse('sign-up'), data={
            "username": "ahmedsaleh",
            "password": "Test123456!!",
            "email": "ahmedsaleh@gmail.com",
            "first_name": "Ahmed",
            "last_name": "Saleh"
        })
        new_user = new_user_response.json()

        self.client.credentials(HTTP_AUTHORIZATION=self.token)

        data = {
            "avatar": "https://pbs.twimg.com/profile_banners/1236621082213462016/1674966722/1500x500"
        }

        response = self.client.put(
            reverse('users-detail', kwargs={'pk': new_user['data']['id']}), data=data)
        result = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            result['detail'], 'You do not have permission to perform this action.')

    def test_create_users_with_no_permission_throws_exception(self):
        data = {
            "username": "fadezak100",
            "password": "Password123456!!",
            "email": "fadezak100w@gmail.com",
            "first_name": "Micheal",
            "last_name": "Scott"
        }

        response = self.client.post(reverse('users-list'), data=data)
        result = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            result['detail'], 'Authentication credentials were not provided.')

    def test_validate_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

        response = self.client.post(reverse('authenticate_token'))
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['user']['username'], 'fadezak100')

    def test_validate_token_throws_exception(self):
        token = 'Token 484f085d6c12b1ae2b27748d3ba5429d3a762904e1e15e3aa68a8a1eb0212a6d'
        self.client.credentials(HTTP_AUTHORIZATION=token)

        response = self.client.post(reverse('authenticate_token'))
        result = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(result['detail'], 'Invalid token.')
