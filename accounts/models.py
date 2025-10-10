from django.db import models
import re
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UsersManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)  # ✅ hashes password properly
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, first_name, last_name, password, **extra_fields)

    def user_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$')

        if not postData.get('first_name'):
            errors['first_name_empty'] = 'First Name is Empty'
        elif len(postData['first_name']) < 2:
            errors['first_name_len'] = 'First Name must be more than 2 characters'

        if not postData.get('last_name'):
            errors['last_name_empty'] = 'Last Name is Empty'
        elif len(postData['last_name']) < 2:
            errors['last_name_len'] = 'Last Name must be more than 2 characters'

        if not postData.get('email'):
            errors['email_empty'] = 'Email is Empty'
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invalid email address'
        elif Users.objects.filter(email=postData['email']).exists():
            errors['email_exist'] = "Email already registered"

        if not postData.get('password') or not postData.get('confirm_PW'):
            errors['password_empty'] = 'Password is Empty'
        elif len(postData['password']) < 8:
            errors['password_len'] = 'Password should be more than 8 characters'
        elif postData['password'] != postData['confirm_PW']:
            errors['password_confirm'] = 'Passwords do not match'

        return errors

    def login_validator(self, postData):
        errors = {}
        if not postData.get('email'):
            errors['email_empty'] = 'Email is Empty'
        if not postData.get('password'):
            errors['password_empty'] = 'Password is Empty'
        # You don’t need "user_email" key check here. Validation should happen in the view with authenticate().
        return errors


class Users(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    # ✅ Required by Django
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UsersManager()

    USERNAME_FIELD = "email"   # use email instead of username
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
