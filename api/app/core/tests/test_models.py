from datetime import date
from django.test import TestCase
from django.contrib.auth import get_user_model
from campaigns.models import Campaign, GameSession


def sample_user(email='test@test.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class TestUserModel(TestCase):
    def test_create_user_with_email_success(self):
        """Test creating new user with email is successful"""
        email = "test@testemail.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the new user email is normalized"""
        email = "test@TESTAPP.com"
        user = get_user_model().objects.create_user(email, 'test123')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating new user with no email raises Error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_superuser(self):
        """Test Creating superuser"""
        user = get_user_model().objects.create_superuser(
            email='test@testapp.com',
            password='test123'
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

class TestCampaignModel(TestCase):
    def test_campaign_str(self):
        """Test Campaign string representation"""
        campaign = Campaign.objects.create(
            user=sample_user(),
            name="Dnd Campaign",
        )

        self.assertEqual(str(campaign), campaign.name)


class TestGameSessionModel(TestCase):
    def setUp(self):
        self.user = sample_user()
        self.campaign = Campaign.objects.create(
            user=self.user,
            name="DnD Campaign"
        )
        self.game_session = GameSession.objects.create(
            campaign=self.campaign,
            name="Session 1"
        )

    def test_game_session_str(self):
        """Test GameSesion String representation"""

        self.assertEqual(str(self.game_session), self.game_session.name)

    def test_game_session_attrs(self):
        """Test GameSession Attributes"""
        self.assertIsNone(self.game_session.end_time)

        self.game_session.end_time = date.today()
        self.assertGreater(
            self.game_session.start_time,
            self.game_session.end_time
        )



