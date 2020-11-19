from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.indexes import BrinIndex
from django.core.exceptions import ValidationError
from django.db import models, router
from django.conf import settings
from django.db.models import F, Q, Sum, Prefetch
import datetime
import six
from django.utils import timezone
from django.db import models
from django.core.validators import MaxValueValidator, \
    MinValueValidator  # not an actual unit test, but some validation for break_length
from django.db.models.signals import post_save
from django.dispatch import receiver

User = settings.AUTH_USER_MODEL
INFLATION_ASSUMPTION = 0.025


def get_current_year():
    return datetime.date.today().year


def get_previous_year():
    current_year = datetime.date.today().year
    # return get_current_year() - 1
    return current_year - 1


def get_current_date():
    return datetime.date.today()


class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    identifier = models.CharField(max_length=40, unique=True)
    date_of_birth = models.DateField()
    salary = models.FloatField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        # "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        # "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class ContactInfo(models.Model):
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=30, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class Profile(models.Model):
    """
    If you’re starting a new project, it’s highly recommended to set up a custom user model,
    even if the default User model is sufficient for you. This model behaves identically to the default user model,
    but you’ll be able to customize it in the future if the need arises
    https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)
    MALE, FEMALE = 'M', 'F'
    choices = (
        (MALE, 'Male'),
        (FEMALE, 'Female'))
    gender = models.CharField(max_length=1, choices=choices, blank=True, null=True, verbose_name='Gender')

    def __str__(self):
        return self.user.username


class Test(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='Career Name')
    industry = models.CharField(max_length=128, blank=True, null=True)
    occ_title = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return str(self.name)