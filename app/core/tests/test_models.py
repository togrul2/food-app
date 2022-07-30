"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


User = get_user_model()


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = User.objects.create_user(email, password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test user email is normalized for new users."""
        sample_emails = [
            ('test1@EXAMPLE.com', 'test1@example.com'),
            ('Test2@Example.com', 'Test2@example.com'),
            ('TEST3@EXAMPLE.COM', 'TEST3@example.com'),
            ('test4@example.COM', 'test4@example.com')
        ]
        for email, expected in sample_emails:
            user = User.objects.create_user(email, 'sample123')
            with self.subTest():
                self.assertEqual(user.email, expected)

    def test_user_without_email(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            User.objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        email = 'test123@example.com'
        password = 'test123'
        user = User.objects.create_superuser(email, password)

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)