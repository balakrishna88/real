from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, phone_number=None, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        
        if not username:
            raise ValueError("Username is required")
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,  # Add phone_number to the model
            **extra_fields  # Allow additional fields to be passed
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, username, email, password, **extra_fields):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
    

class Account(AbstractBaseUser):
    # Core Fields
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    username        = models.CharField(max_length=50, unique=True)
    email           = models.EmailField(max_length=100, unique=True)  # Changed to EmailField
    phone_number    = models.CharField(max_length=15, blank=True, null=True)

    # Additional Fields
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    country         = models.CharField(max_length=50, blank=True, null=True)
    state           = models.CharField(max_length=50, blank=True, null=True)
    district        = models.CharField(max_length=50, blank=True, null=True)
    location        = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth   = models.DateField(blank=True, null=True)
    bio             = models.TextField(blank=True, null=True)
    website         = models.URLField(blank=True, null=True)

    # Social Media Links (Stored as JSON)
    social_media_links = models.JSONField(
        default=dict,
        blank=True,
        null=True,
        help_text="Store social media links as a JSON object. Example: {'facebook': 'https://facebook.com/user', 'instagram': 'https://instagram.com/user'}"
    )

    # Required Fields
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now=True)  # Changed to auto_now
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)  # Changed default to True
    is_superadmin   = models.BooleanField(default=False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    objects = MyAccountManager()
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True