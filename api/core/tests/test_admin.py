from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        """Add new User, Have them  logged in"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="test@test.com",
            password="test123"
        )

        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="user@test.com",
            password="123test",
            name="Jon Doe"
        )

    def test_users_listed(self):
        """Test users are listed on user page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        # check response contains a certain item...
        # smart to check output of res (given if 200)
        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.name)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        # /admin/core/user/1
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
