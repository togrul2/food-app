"""
Serializers for the user API View.
"""
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import (
    get_user_model,
    authenticate
)

from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = User
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a new user."""
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return the user instance."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={
            'input_type': 'password',
            'trim_whitespaces': False
            }
        )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password
        )
        if not user:
            message = _("Unable to authenticate with provided credentials.")
            raise serializers.ValidationError(message, code='authorization')

        attrs['user'] = user
        return attrs
