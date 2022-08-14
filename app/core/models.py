"""
Database models.
"""

from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """User manager for user model."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create, save and return a new superuser."""
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model."""
    email = models.EmailField(_('email'), max_length=255, unique=True)
    name = models.CharField(_('name'), max_length=255)
    is_active = models.BooleanField(_('is active'), default=True)
    is_staff = models.BooleanField(_('is staff'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Recipe(models.Model):
    """Recipe model."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('User')
    )
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    time_minutes = models.IntegerField(_('time in minutes'))
    price = models.DecimalField(_('price'), max_digits=5, decimal_places=2)
    link = models.CharField(_('link'), max_length=255, blank=True)
    tags = models.ManyToManyField('Tag', verbose_name=_('tags'),
                                  related_name='recipes')
    ingredients = models.ManyToManyField('Ingredient',
                                         verbose_name=_('indgredients'))

    def __str__(self):
        return self.title


class Tag(models.Model):
    """Tag for filtering recipes."""
    name = models.CharField(_('name'), max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name=_('user'))

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient model for recipes."""
    name = models.CharField(_('name'), max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('User')
    )

    class Meta:
        verbose_name = _('ingredient')
        verbose_name_plural = _('ingredients')

    def __str__(self):
        return self.name
