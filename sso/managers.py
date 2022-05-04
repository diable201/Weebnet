from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class NotDeletableManagerMixin(models.Manager):
    DELETE_FIELD = 'is_deleted'

    def filter(self, with_deleted=False, *args, **kwargs):
        if with_deleted:
            super().filter(*args, **kwargs)
        if self.DELETE_FIELD not in kwargs:
            kwargs[self.DELETE_FIELD] = False
        return super().filter(*args, **kwargs)

    def exclude(self, with_deleted=False, *args, **kwargs):
        if with_deleted:
            super().exclude(*args, **kwargs)
        if self.DELETE_FIELD not in kwargs:
            kwargs[self.DELETE_FIELD] = False
        return super().exclude(*args, **kwargs)

    def all(self, with_deleted=False):
        if not with_deleted:
            return super().filter(deleted=False)
        return super().all()

    def get(self, with_deleted=False, *args, **kwargs):
        if with_deleted:
            super().filter(*args, **kwargs)
        if self.DELETE_FIELD not in kwargs:
            kwargs[self.DELETE_FIELD] = False
        return super().get(*args, **kwargs)


class ActiveUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class NotDeletableModelMixin(models.Model):
    DELETE_FIELD = 'is_deleted'

    class Meta:
        abstract = True

    is_deleted = models.BooleanField(default=False)

    def delete(self, using=None, *args, **kwargs):
        setattr(self, self.DELETE_FIELD, True)
        self.save(using=using, update_fields=[self.DELETE_FIELD])

    def __str__(self):
        if getattr(self, self.DELETE_FIELD):
            return gettext("DELETED ")
        return ""
