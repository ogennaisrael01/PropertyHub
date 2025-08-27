from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser, PermissionsMixin
from django.urls import reverse
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
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password, **kwargs):
        """ Create and return a super user with email and password """

        user = self.create_user(email=email, password=password, **kwargs)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)

        return user
    
class CustomUser(AbstractUser, PermissionsMixin):
    objects = CustomUserManager()

    email = models.EmailField(max_length=50, unique=True, null=False)
    username = models.CharField(max_length=40, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    


    role = models.CharField(
        max_length=100, 
        blank=False,
        null=False,
        help_text="Tenant or Owner"
        )
    
    REQUIRED_FIELDS = ["username", "role"]
    def __str__(self):
        return self.get_username()

    @property
    def is_superuser(self):
        # Returns a super user 
        return self.is_admin

class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE,
        related_name="user_profile")
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=250, blank=True)
    profile_picture = models.ImageField(upload_to="user_profile", null=True, blank=True)

    @property
    def get_full_name_or_username(self):
        """ 
        Get full name of that user else returns the username
        """
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return self.user.username
    
    def __str__(self):
        """
        - String representation of the user object.
        - Returns the username of that object.
        """
        return self.user.email
    
    def get_absolute_url(self):
        """
        - Returns a URL for the user profile.
        """
        return reverse("profile", kwargs={"pk": self.pk})
    