from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser, PermissionsMixin
import uuid
from phonenumber_field.modelfields import PhoneNumberField

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
    
    def create_superuser(self, email, password, **extra_fields):
        """ Create and return a super user with email and password """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("A super user filed must be set to True")
        if not extra_fields.get("is_superuser"):
            raise ValueError("A super user nust have is_superuser field set to True")
        
        user = self.create_user(email=email, password=password, **extra_fields)
        return user
    
class CustomUser(AbstractUser, PermissionsMixin):
    class RoleChoices(models.TextChoices):
        TENANT = 'TENANT', "Tenant"
        OWNER = 'OWNER', "Owner"

    user_id = models.UUIDField(primary_key=True, unique=True, db_index=True, default=uuid.uuid4())
    email = models.EmailField(unique=True, max_length=200)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(max_length=100, choices=RoleChoices.choices, default=RoleChoices.OWNER)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]
    objects = CustomUserManager()

    class Meta:
        verbose_name = "user"
        db_table = "users"
        indexes = [
            models.Index(fields=["email"], name="email_idx"),

        ]
    
    
    def __str__(self):
        return f"CustomUser('{self.email}', {self.get_username()}, {self.role})"

    @property
    def is_admin(self):
        return self.is_superuser

class Profile(models.Model):
    profile_id = models.UUIDField(primary_key=True, db_index=True, unique=True, default=uuid.uuid4())
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    phone_number = PhoneNumberField(blank=False)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    address = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        - String representation of the user object.
        - Returns the email of that object.
        """
        return f"Profile('{self.user.email}', {self.phone_number}, {self.address})"
    
    class Meta:
        db_table = "user_profiles"
    

class Avater(models.Model):
    avater_id = models.UUIDField(primary_key=True, null=False, default=uuid.uuid4(), db_index=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="avater")
    image_url = models.ImageField(null=True)
    caption = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Avater('{self.image_url}', {self.caption}, {self.created_at.strftime("%d %B %Y")})"
    
