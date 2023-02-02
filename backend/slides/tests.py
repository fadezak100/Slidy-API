from django.test import TestCase
from rest_framework.test import APITestCase
from knox.models import AuthToken
from users.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

class SlidesTests(APITestCase):


    def setUp(self):
        self.user = User.objects.create(username='fadezak100',
                                        password='Test123456!!',
                                        email='fadezak100@gmail.com',
                                        first_name='fadi',
                                        last_name='zakout')

        self.token = f'Token {str(AuthToken.objects.create(user=self.user)[1])}'


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

    def test_upload_other_files_extension(self):
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


    def test_upload_and_unauthorized(self):
        file = SimpleUploadedFile("test.md", b"file_content")

        data = {
                "title": "new presentation",
                "description": "this is the new file description",
                "slide": file
        }

        response = self.client.post(reverse("slides-list"), data=data)
        self.assertEqual(response.status_code, 401)