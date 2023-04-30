from django.contrib.auth.base_user import BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, phone_number, email, password, first_name=None, last_name=None, client=None, **extras):
        """
        Creates and saves a User with the given email and password.
        """
        if not phone_number:
            raise ValueError('Users must have an phone number')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            client=client,
            **extras
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, phone_number, email, password, first_name=None, last_name=None, client=None):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            client=client
        )
        user.client_rep = False
        user.staff = True
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, password, first_name=None, last_name=None, client=None, ):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            client=client
        )
        user.client_rep = False
        user.staff = True
        user.admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class CustomModelManager(models.Manager):
    def get_or_null(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None
