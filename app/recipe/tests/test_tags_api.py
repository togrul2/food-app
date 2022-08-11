"""
Tests for the tags API.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from recipe.serializers import TagSerializer


User = get_user_model()
TAGS_URL = reverse('recipe:tag-list')


def detail_url(tag_id):
    """Return a url for tag detail."""
    return reverse('recipe:tag-detail', args=[tag_id])


def create_user(email='user@example.com', password='testpassword123'):
    """Create and return a user."""
    return User.objects.create_user(email=email, password=password)


class PublicTagsApiTests(TestCase):
    """Test unauthenticated API request."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving tags."""
        response = self.client.get(TAGS_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving a list of tags."""
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        response = self.client.get(TAGS_URL)
        tags = Tag.objects.all().order_by('-name')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_tag_limited_to_user(self):
        """Test list of tags is limited to authenticated user."""
        user2 = create_user('user2@example.com')
        Tag.objects.create(user=user2, name='Fruity')
        tag = Tag.objects.create(user=self.user, name='Comfort Food')

        response = self.client.get(TAGS_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], tag.name)
        self.assertEqual(response.data[0]['id'], tag.id)

    def test_update_tag(self):
        """Test updating a tag."""
        tag = Tag.objects.create(user=self.user, name='After Dinner')
        payload = {'name': 'Dessert'}
        url = detail_url(tag.id)
        response = self.client.patch(url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload['name'])

    def test_delete_tag(self):
        """Test deleting a tag."""
        tag = Tag.objects.create(user=self.user, name='Breakfast')
        url = detail_url(tag.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        tags = Tag.objects.filter(user=self.user)
        self.assertFalse(tags.exists())