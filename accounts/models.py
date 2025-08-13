from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
# Create your models here.

class CustomUserManager(BaseUserManager):
    """ Custom user manager for  creating CustomUser model  """
    def create_user(self, email, password, **kwargs):
        """ create and returns a user with email and password """

        if not email:
            raise ValueError("Please enter your email address")
        if not password:
            raise ValueError("Please enter your password")
        
        email = self.normalize_email(email)
        user = self.model(email=email, password=password, **kwargs)
        user.set_password(password)
        user.save(using=self.db)

        return user
    
    def create_superuser(self, email, password, **kwargs):
        """ Create and return a super user with email and password """

        user = self.create_user(email=email, password=password, **kwargs)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self.db)

        return user
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    objects = CustomUserManager()

    email = models.CharField(max_length=50, unique=True, null=False)
    username = models.CharField(max_length=40, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.get_username()

