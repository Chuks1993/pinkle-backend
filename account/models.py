import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

#  switch username to email for ussr login
# https://tech.serhatteker.com/post/2020-01/email-as-username-django/
# complex user model
# https://programtalk.com/vs2/?source=python/9690/otm-legacy/profiles/models.py


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, models.Model):
    username = None
    email = models.EmailField(verbose_name=_("User email"), help_text=("Required"), unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    zip_code = models.CharField(_("zip code"), max_length=5, null=True, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    grade = models.CharField(max_length=3)


# class AddressField(models.Model):
#     address_1 = models.CharField(_("address"), max_length=128)
#     address_2 = models.CharField(_("address cont'd"), max_length=128, blank=True)

#     city = models.CharField(_("city"), max_length=64, default="Dallas")
#     state = USStateField(_("state"), default="TX")
#     zip_code = models.CharField(_("zip code"), max_length=5, default="75244")
