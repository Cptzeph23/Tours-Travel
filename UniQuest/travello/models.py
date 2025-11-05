from django.db import models
from cloudinary.models import CloudinaryField
# Create your models here.

class Destination(models.Model):
    name = models.CharField(max_length=100)
    img = CloudinaryField(
        'image',
        folder='destinations',  # Organize images in a folder
        use_filename=True,      # Use original filename
        unique_filename=False,  # Don't make unique if same filename
        overwrite=True          # Overwrite if same filename
    )
    desc = models.TextField()
    price = models.IntegerField()
    offer = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
