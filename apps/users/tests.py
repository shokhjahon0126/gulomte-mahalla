from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from apps.users.models import User, UserRole


class UserAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testadmin',
            password='oldpassword123',
            full_name='Test Admin',
            role=UserRole.ADMIN
        )
        self.client.force_authenticate(user=self.user)

    def test_get_user_profile(self):
        url = reverse('users:user-profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testadmin')
        self.assertEqual(response.data['full_name'], 'Test Admin')
        self.assertEqual(response.data['role'], 'admin')

    def test_update_user_profile(self):
        url = reverse('users:user-profile')
        data = {'username': 'updatedadmin', 'full_name': 'Updated Admin'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.full_name, 'Updated Admin')
        self.assertEqual(self.user.username, 'updatedadmin')

    def test_change_password_success(self):
        url = reverse('users:change-password')
        data = {
            'new_password': 'newpassword123',
            'confirm_new_password': 'newpassword123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))

    def test_change_password_mismatch(self):
        url = reverse('users:change-password')
        data = {
            'new_password': 'newpassword123',
            'confirm_new_password': 'differentpassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('confirm_new_password', response.data)
