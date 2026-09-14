from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from apps.users.models import User, UserRole
from apps.news.models import News


class NewsAPITestCase(APITestCase):
    def setUp(self):
        # Admin user
        self.admin_user = User.objects.create_user(
            username='admin_news',
            password='adminpassword123',
            full_name='Admin News',
            role=UserRole.ADMIN
        )

        # Initial news item
        self.news_item = News.objects.create(
            title='First News Title',
            description='First News Description'
        )

    def test_anonymous_user_can_get_news_list(self):
        url = reverse('news:news-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_anonymous_user_can_get_news_detail(self):
        url = reverse('news:news-detail', kwargs={'pk': self.news_item.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'First News Title')

    def test_anonymous_user_cannot_create_news(self):
        url = reverse('news:news-list')
        data = {'title': 'Anon Title', 'description': 'Anon Description'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_user_can_create_news(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('news:news-list')
        data = {'title': 'Admin Created Title', 'description': 'Admin Created Description'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(News.objects.count(), 2)

    def test_admin_user_can_update_news(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('news:news-detail', kwargs={'pk': self.news_item.pk})
        data = {'title': 'Updated Title', 'description': 'Updated Description'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.news_item.refresh_from_db()
        self.assertEqual(self.news_item.title, 'Updated Title')

    def test_admin_user_can_delete_news(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('news:news-detail', kwargs={'pk': self.news_item.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(News.objects.count(), 0)
