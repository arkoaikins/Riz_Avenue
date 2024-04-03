from django.db import models
from userauths.models import User
from django.utils.text import slugify


# # Create your models here.


class Brand(models.Model):
    """
    Model representing a brand
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, related_name="vendor"
    )
    image = models.FileField(
        upload_to="brand", default="avenue-image.jpg", blank=True)
    name = models.CharField(
        max_length=100, help_text="Brand Name", null=True, blank=True
    )
    email = models.EmailField(
        max_length=100, help_text="Brand Email", null=True, blank=True
    )
    description = models.TextField(null=True, blank=True)
    mobile = models.CharField(
        max_length=150, help_text="Brand Mobile number", null=True, blank=True
    )
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=5000)

    class Meta:
        verbose_name_plural = "Brands"
        ordering = ["-date"]

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        """
        Custom save method to auto-generate slug if not provided.
        """
        if self.slug is None or self.slug == "":
            self.slug = slugify(self.name)
        super(Brand, self).save(*args, **kwargs)
