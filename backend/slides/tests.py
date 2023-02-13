from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from knox.models import AuthToken
from rest_framework.test import APITestCase

from users.models import User
from .models import Slide


class SlidesTests(APITestCase):

    def setUp(self):
        file = SimpleUploadedFile("test.md", b"file_content")

        self.user = User.objects.create(
            username='fadezak100',
            password='Test123456!!',
            email='fadezak100@gmail.com',
            first_name='fadi',
            last_name='zakout'
        )

        self.token = f'Token {str(AuthToken.objects.create(user=self.user)[1])}'
        self.slide = Slide.objects.create(
            user=self.user,
            title='new presentation',
            description='this is the description of the new slide',
            slide=file,
            url='http://res.cloudinary.com/diujf6140/raw/upload/v1675258547/fqv1cmj5mzv20v6krdqj.md',
            is_live=True,
            is_public=True
        )

    def test_get_slides(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(reverse('slides-list'))

        self.assertEqual(response.status_code, 200)

    def test_upload_slides(self):
        file = SimpleUploadedFile("test.md", b"file_content")

        data = {
            "title": "new presentation",
            "description": "this is the new file description",
            "slide": file
        }
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(reverse("slides-list"), data=data)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(result['data']['url'].find('cloudinary'))

    def test_upload_other_files_extension_throws_exception(self):
        file = SimpleUploadedFile("test.exe", b"file_content")

        data = {
            "title": "new program",
            "description": "this is the new file with extension of .exe",
            "slide": file
        }

        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(reverse("slides-list"), data=data)
        result = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(result.get('slide')[0], 'only .md files are allowed')

    def test_upload_and_unauthorized_throws_exception(self):
        file = SimpleUploadedFile("test.md", b"file_content")

        data = {
            "title": "new presentation",
            "description": "this is the new file description",
            "slide": file
        }

        response = self.client.post(reverse("slides-list"), data=data)
        self.assertEqual(response.status_code, 401)

    def test_delete_slide(self):
        file = SimpleUploadedFile("test.md", b"file_content")

        data = {
            "title": "new presentation",
            "description": "this is the new file description",
            "slide": file
        }
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(reverse("slides-list"), data=data)

        response = self.client.delete(
            reverse("slides-detail", kwargs={'pk': self.slide.id}), data=data)

        self.assertEqual(response.status_code, 204)

    def test_delete_others_slide_throws_excpetion(self):
        file = SimpleUploadedFile("test.md", b"file_content")

        new_user = User.objects.create(
            username='ahmed',
            password='Test123456!!',
            email='ahmed@gmail.com',
            first_name='ahmed',
            last_name='saleh')

        new_user_token = f'Token {str(AuthToken.objects.create(user=new_user)[1])}'

        self.client.credentials(HTTP_AUTHORIZATION=new_user_token)

        data = {
            "title": "new presentation",
            "description": "this is the new file description",
            "slide": file
        }

        response = self.client.post(reverse("slides-list"), data=data)
        new_slide = response.json()

        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.delete(
            reverse("slides-detail", kwargs={'pk': new_slide['data']['id']}), data=data)
        result = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            result['detail'], 'You do not have permission to perform this action.')

    def test_delete_not_existed_slide_throws_exception(self):
        file = SimpleUploadedFile("test.md", b"file_content")

        data = {
            "title": "new presentation",
            "description": "this is the new file description",
            "slide": file
        }
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(reverse("slides-list"), data=data)

        response = self.client.delete(
            reverse("slides-detail", kwargs={'pk': 10}), data=data)
        result = response.json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(result['detail'], 'Not found.')

    def test_retrieve_slide(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

        response = self.client.get(
            reverse('slides-detail', kwargs={'pk': self.slide.id}))
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('html_content', result)

    def test_not_existed_retrieve_slide_throws_exception(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

        response = self.client.get(reverse('slides-detail', kwargs={'pk': 4}))
        result = response.json()


        self.assertEqual(response.status_code, 404)
        self.assertIn(result['detail'], 'Not found.')

    def test_list_own_slides(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

        response = self.client.get(reverse('slides-list'))
        self.assertEqual(response.status_code, 200)

    def test_list_and_unauthenticated_throws_exception(self):
        response = self.client.get(reverse('slides-list'))
        result = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            result['detail'], 'Authentication credentials were not provided.')

    def test_update_own_slides(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

        update_data = {
            "title": "updated title",
            "is_public": False,
            "is_live": False
        }

        response = self.client.patch(
            reverse('slides-detail', kwargs={'pk': self.slide.id}), data=update_data)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['data']['title'], update_data['title'])
        self.assertEqual(result['data']['is_public'], update_data['is_public'])
        self.assertEqual(result['data']['is_live'], update_data['is_live'])

    def test_update_others_slides_throws_exception(self):
        file = SimpleUploadedFile("test.md", b"file_content")

        new_user = User.objects.create(
            username='ahmed',
            password='Test123456!!',
            email='ahmed@gmail.com',
            first_name='ahmed',
            last_name='saleh'
        )

        new_user_token = f'Token {str(AuthToken.objects.create(user=new_user)[1])}'

        self.client.credentials(HTTP_AUTHORIZATION=new_user_token)

        data = {
            "title": "new presentation",
            "description": "this is the new file description",
            "slide": file
        }

        response = self.client.post(reverse("slides-list"), data=data)
        new_slides = response.json()

        update_data = {
            "title": "updated title",
            "is_public": False,
            "is_live": False
        }
        
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.patch(
            reverse("slides-detail", kwargs={'pk': new_slides['data']['id']}), data=update_data)

        result = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            result['detail'], 'You do not have permission to perform this action.')

    def test_update_not_existed_slide_throws_exception(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

        update_data = {
            "title": "updated title",
            "is_public": False,
            "is_live": False
        }
        response = self.client.patch(
            reverse("slides-detail", kwargs={'pk': 10}), data=update_data)
        result = response.json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(result['detail'], 'Not found.')
