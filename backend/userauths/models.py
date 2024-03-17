from django.db import models
from django.contrib.auth.models import AbstractUser
from shortuuid.django_fields import ShortUUIDField

# Create my custom user model.
class User(AbstractUser):
    """
    A custom user model that uses email for authentication and stores
    other user details
    """
    username = models.CharField(unique=True, max_length=100)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        """
        Returns a user-friendly representation of the
        User object
        """
        return self.email
    
    def save(self, *args, **kwargs):
        """
        Pre-save hook to ensure username and full name are
        populated from email if empty
        """
        email_username, other = self.email.split("@")
        if not self.full_name:
            self.full_name = email_username
        if not self.username:
            self.username = email_username

        super().save(*args, **kwargs)
        
#create profile model
class Profile(models.Model):
    """
    Model to store user profile information linked to the 
    User model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to="image", default="default/default-user.jpg", null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvwxyz")
    
    def __str__(self):
        """Returns a user-friendly representation of a Profile"""
        if self.full_name:
            return str(self.full_name)
        else:
            return str(self.user.full_name)
        
    def save(self, *args, **kwargs):
        """Pre-save hook to populate profile's full name from User model if empty"""
        if not self.full_name:
            self.full_name = self.user.full_name
        
        super().save(*args, **kwargs)